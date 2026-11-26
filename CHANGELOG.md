# Changelog

Significant merged changes to Oppy are recorded here. The source identifies itself as version `0.1.0`. These dates describe development history, not separate tagged releases. Proposed work belongs in issues.

## [Unreleased]

### Added

- Read-only `status --json` output for monitoring scripts.

- Optional English Telegram notifications and summary preview via `BEACON_NOTIFICATION_LANGUAGE=en`. Brazilian Portuguese remains the default.

- Contribution guide, code of conduct, security reporting policy, bilingual issue templates and an English pull request template.

### Changed

- Refresh README installation, configuration, updates, backups, source limitations and contributor onboarding. No runtime behavior changed.

## 2026-11-21 — Reliability review

### Fixed

- Bound restart waits for very long stored Retry-After values; retain only complete diagnostic snapshot pairs without removing unrelated files. Clarify Portuguese registration labels and notification wording ([#13](https://github.com/kayo-willian/oppy/pull/13)). The PR reports 63 passing offline tests.

## 2026-11-20 — Oppy rename and diagnostics

### Added

- Save rejected HTML and metadata as bounded, private diagnostic snapshots and expose their location in status ([#12](https://github.com/kayo-willian/oppy/pull/12)).

### Changed

- Rename OpportunityBeacon to Oppy, add the original cover and retain the existing SQLite schema, database path, environment settings and Docker volume ([#10](https://github.com/kayo-willian/oppy/pull/10)).
- Clarify the single supported source and personal Telegram bot setup ([#11](https://github.com/kayo-willian/oppy/pull/11)).

## 2026-11-19 — Initial functional milestone

### Added

- Python and SQLite foundation, persistent Compose storage and offline CI ([#1](https://github.com/kayo-willian/oppy/pull/1), [#3](https://github.com/kayo-willian/oppy/pull/3)).
- PSG source reconnaissance, sanitized fixtures, normalized snapshots and course matching ([#2](https://github.com/kayo-willian/oppy/pull/2), [#4](https://github.com/kayo-willian/oppy/pull/4), [#5](https://github.com/kayo-willian/oppy/pull/5)).
- Atomic state changes, persistent notification outbox, scheduler, bounded HTTP, Telegram delivery, local status and SQLite backup ([#6](https://github.com/kayo-willian/oppy/pull/6), [#7](https://github.com/kayo-willian/oppy/pull/7)).
- Tolerant HTML parsing, stage-specific smoke diagnostics, detailed Portuguese notifications and saved-state summaries ([#8](https://github.com/kayo-willian/oppy/pull/8), [#9](https://github.com/kayo-willian/oppy/pull/9)).

[Unreleased]: https://github.com/kayo-willian/oppy/commits/main/
