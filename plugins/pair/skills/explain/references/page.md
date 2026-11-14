# explain page data

The page data is one JSON file the script `scripts/explain-page` turns into the page.

## JSON shape

Text fields take `` `code` ``, `**bold**` and `{{term-id}}` or `{{term-id|label}}`; the page glosses a term at its first `{{…}}` and shows the bare term after.

- `kind`: what the page explains, `ticket` (the default), `flow`, `module` or `diff`; the page's labels follow it (« ce module », « le changement »)
- `project` and `domain` (from the profile, when there is one: the page's AI prompts use them), `source` (`{root, ref?}`: `root` is the folder the repos are cloned in, the profile's `repos_root` or the parent of the current repo; `ref` is the local ref the code is read from, `HEAD` for a flow or a module, left out to read each repo's default branch on origin)
- `key` and `url` (a ticket's key and link, a pull request's number and link; left out for a flow or a module), `short` (2-4 words: the tab title is `<key> <short>`, or `short` alone), `title` (one sentence: what the ticket does, or what the flow or the module is for; the bar shows it with its `{{…}}` as plain words), `summary` (60 words or fewer: today versus after, or what it does), `depth` (`full` or `léger`), `sources` (`[{label, url?}]`)
- `glossary`: `[{id, term, def, what, why, here, example, related?, code?}]`, every term the text tags. A tagged term is a button that opens the context panel ("Ça mange quoi en hiver ?"): `what` (what it is, in the project's domain or in the code), `why` (why it exists), `here` (its role in this subject), `example` (one concrete case), `related` (other term ids); one or two sentences each, from sources like the rest. `def` is the one-line hover title. `code: true` sets the term in monospace
- Départ: `tldr` (2 or 3 bullets the summary doesn't say: where it lands, the biggest trap, what to check first), `product` (`{before: [], after: []}`, for a ticket or a diff; left out for a flow or a module, whose summary then folds under « En résumé »), `need` (paragraphs, 120 words or fewer; they fold under « Le besoin », and `summary` and `product` under « Aujourd'hui et après le ticket »), `links` (see The trip map), `tickets` (see Tickets), `reading` (`[{repo, path, line, why}]`)
- Stations: `flow` (`[{station, layer, simple, tech, cite, changed?, pic, code?, plan?, diff?, repo?}]`). `station` is the real identifier the station is named after; `layer` is where the hop runs, one of `frontend`, `gateway`, `backend`, `data`, shown in parentheses beside the name. `pic` is a Mermaid `flowchart TB` of 3 or 4 nodes around that hop with short labels, the hop's own node marked `class <id> here` (the page fills it in the station's line colour); `real`, `gone` and `gap` mark what changes, disappears or is missing. `code` is `{repo, path, start, end, mark?}` (`mark`: line numbers to highlight); the line colour comes from `code.repo`, or `repo` on a hop without code. `diff` is a sketch with `+ `, `- ` and two-space line prefixes
- Terminus: `traps` (`[{title, text, cite?, inference?, blocking?}]`, `text` 50 words or fewer), `questions` (strings: what the ticket leaves unsaid, or what the code does not say about itself; the input of the grilling). The page holds no questions for the reader: the « redis-le-moi » happens in the chat.

The page skips empty parts. The script warns when a budget above is exceeded (its constants hold them), when more than 4 traps have none `blocking`, and when a link label runs past 26 characters; it refuses a link or a ticket that points outside the stations.

## The trip map (Départ)

Départ is a mental map before it is text: the first screen holds the title, the TLDR and the top of the trip map; the summary, avant/après, the need and the ticket list fold under the map. The reader should be able to point at any station and say which repo it lives in, what it does, and which ticket touches it.

The page draws the map from `flow` itself, in the strip's own language: one lane per repo (in the order the trip meets them, named on a pin that stays in view), the stations as ringed circles in trip order, a double ring where the trip changes repo, and each station a link to its screen. Nothing is drawn by hand, so the map and the strip can never disagree.

- **Avant / Après** share one layout. Après dashes the ring of the stations the ticket leaves alone, sets the changed names in orange, and pins under each station the tickets that touch it (from `tickets`), with one dashed « aucun ticket » when an uncovered piece lands there.
- **`links`** marks a segment between two consecutive stations that is not a direct call: `[{from, to, label, missing?, after?}]`. The segment is dotted, grey for a jump in time or context (`"ensuite, à la soumission"`), orange with `missing: true` for a link that should exist and does not (`"aucun lien aujourd'hui"`). `after` names what the ticket builds there (`"pont à créer, aucun ticket"`): Après draws that segment dashed in its line's colour, under that label. Labels are 26 characters or fewer and sit in the lower station's lane, clear of the tickets.
- Order `flow` so the trip reads left to right as the user lives it, and split two flows that never call each other with a `links` entry rather than pretending one calls the other.
- Station pictures stay Mermaid `flowchart TB`, 3 or 4 nodes with short labels, so they read large. When the flow is one that `ns diagram` already draws (`ns diagram list`), start the pictures from that diagram's source (`ns diagram <id>`).

### Tickets

`tickets` places the work on the trip, for an initiative, an epic, or a ticket with sub-tasks: `[{key, title, status, stations?, children: [{key, title, status, stations} | {gap: true, title, stations}]}]`. `stations` are the station numbers the ticket touches (the script refuses one out of range); each shows as a dot in its line colour that jumps to the station. A `gap` child names a piece of the trip that no ticket covers yet, drawn dashed. Statuses are Jira's, verbatim. Leave `tickets` out for a single ticket with no children.
