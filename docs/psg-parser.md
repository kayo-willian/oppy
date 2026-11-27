# Offline PSG parsing

[Português (Brasil)](../pt-BR/docs/psg-parser.md) · [Home](../README.md)

Pass decoded listing HTML to `parse_listing`, then supply a returned selection and its detail HTML to `parse_detail(markup, selection)`. Both functions return a status and reason. Only OK carries records. A missing Santarém panel in a recognizable listing or an unconfirmed empty list is INCONCLUSIVE. Malformed structure, conflicting links and contradictory selection metadata are FAILED. Keep the last valid snapshot for either outcome.

Registration timestamps without an offset use America/Santarem by assumption. Course periods are local calendar dates. The registration channel describes how to apply. An in-person control leaves registration status unknown. The fixtures' redacted venue marker represents an unknown venue. Selection documents are recorded once per detail.

Match courses across two snapshots in this order. Each match reserves both observations. Check uniqueness against the full snapshots so an earlier match cannot make a duplicate appear unique.

1. Match a selection-scoped course alias (`data-curso`) that occurs exactly once on each side. This can resolve a title or venue change.
2. Match a unique combination of selection, normalized case-insensitive title and known venue on each side. Missing or corrected course dates do not affect this match.
3. When that combination repeats on either side, use the complete course period (start and end dates) to distinguish classes. The same period must identify exactly one class in that group on each side.

Conflicting known aliases prevent a fallback match. Missing evidence or remaining ambiguity yields `unresolved`. Each match references the previous observation by index. Row order supplies no evidence. No outcome generates a removal or cancellation.

Hashes and field comparisons use the same canonical snapshot: Unicode NFC, collapsed whitespace, ISO dates and timestamps, and deterministic collection order. A field diff returns previous and current canonical values for each changed top-level field. Compare matched courses individually for course-level changes.
