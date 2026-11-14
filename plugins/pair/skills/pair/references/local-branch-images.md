# Local branch images (docker compose stacks)

Run a branch's own code in the local stack before it is pushed: no PR image, no registry. Used for Pre-QA. A project whose stack has its own skill or script for this (the profile's `skills`, `commands.run`) uses that instead; this is the recipe when it has none.

## 1. Build the image

Reuse the service's current image as the runtime, so its config files, certificates and entrypoint stay as the stack expects. Read the entrypoint and architecture first:

```bash
docker image inspect <image> -f '{{json .Config.Entrypoint}} {{.Architecture}}'
```

**A binary that cross-compiles without native dependencies** (a Go service without CGO, a static Rust binary): build it for the image's architecture and copy it over the existing image.

```bash
GOOS=linux GOARCH=<arch> CGO_ENABLED=0 go build -o <scratch>/<binary> ./cmd/<binary>   # from the branch's worktree
printf 'FROM <image>\nCOPY <binary> /app/<binary>\n' > <scratch>/Dockerfile
docker build -t <svc>:<key>-local <scratch>
```

**A service with native dependencies, or an interpreted one**: build in a container from a copy of the worktree, then copy the result over the stack's image. When the repo's own Dockerfile needs secrets for private dependencies, vendor them first from the local cache (`go mod vendor`, a local package cache) so the build needs no network credentials.

```dockerfile
FROM <the language's build image> AS build
WORKDIR /src
COPY . .
RUN <the repo's build command>

FROM <the image the stack runs for this service>
COPY --from=build /src/<build output> /app/<where the entrypoint expects it>
```

Build for the architecture the stack's image has (`docker build --platform linux/<arch>`).

**Data baked into an image** (a seed, embedded schemas) is a second image: a schema change often needs both the service that embeds it and the seeder that loads it. Check which image holds each file before building.

When the branch depends on an unreleased branch of another repo, point it there locally (a `replace`, a path or link dependency) before building. It is a dev-only change: commit the real version bump once that repo is released.

## 2. Run it

Back up the compose override file, then set each service to its local image:

```yaml
services:
  <svc>:
    image: "<svc>:<key>-local"
    pull_policy: never
    platform: linux/<arch>
```

Then recreate those services the way the stack does it (its own script when it has one, so secrets and env files are resolved the same way). A migrations job stays on its published image unless the branch adds a migration: a branch image older than the local database's newest migration fails on it.

## 3. Restore

Once the job is done (`delivery`: at Deliver's close), put back the backed-up override, then recreate the services. Removing only the `image` line leaves `pull_policy: never` and `platform` behind. The local images can stay; `docker image rm <svc>:<key>-local` frees the space.
