---
type: regex
target: last_message
flags: i
match: not_contains
pattern: '(quel|quelle|which|what)[^?\n]{0,80}(ticket|profil|project\.json)[^?\n]{0,60}\?'
---
