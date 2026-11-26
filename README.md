![OPPY pixel-art sign](assets/oppy-cover.svg)

# Oppy

Oppy is a self-hosted monitor that checks public opportunity listings at regular intervals and sends Telegram alerts when listings appear or change. It currently supports one source: Senac Pará’s free course program (PSG) in Santarém.

[![MIT license](https://img.shields.io/badge/license-MIT-blue?style=flat)](LICENSE)
![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat)
![Docker Compose](https://img.shields.io/badge/Docker-Compose-2468a2?style=flat)
![SQLite](https://img.shields.io/badge/storage-SQLite-486477?style=flat)
[![Telegram bot](https://img.shields.io/badge/Telegram-bot-2987ac?style=flat)](https://core.telegram.org/bots)
[![Tests](https://img.shields.io/github/actions/workflow/status/kayo-willian/oppy/tests.yml?branch=main&label=tests&style=flat)](https://github.com/kayo-willian/oppy/actions/workflows/tests.yml)
![Built with vibe coding](https://img.shields.io/badge/built%20with-vibe%20coding-c87824?style=flat)

[Português (Brasil)](pt-BR/README.md) · [Quick start](#quick-start) · [Configuration](#configuration) · [Contributing](#contributing) · [Changelog](CHANGELOG.md)

Oppy is an independent personal project released under the MIT license. Senac Pará is an information source, not a partner or maintainer. Contributions are welcome; development and review times are not guaranteed.

## Supported sources

| Source | Scope | Status |
|---|---|---|
| Senac Pará PSG | Free courses in Santarém, across all subject areas | Implemented |

[Source portal](https://www.pa.senac.br/psg/selecao). Before running live checks, confirm that your intended access is permitted, including recurring polling and linked detail requests. See the [source reconnaissance notes](docs/psg-recon.md). No other source is currently implemented.

## What it does

Oppy compares each collection with the last valid one and records each new listing or change once, so repeated checks do not queue duplicate alerts. A failed check is recorded as a failure and never treated as an empty listing. Oppy sends an alert after consecutive unsuccessful checks and another when collection recovers. It only observes listings and sends notifications. It never submits applications or collects personal information about applicants.

The PSG connector detects new selections and courses, upcoming registration windows, openings, closures, filled places and reopenings. It also tracks revised dates, new documents and amendments.

## How it works

```text
source connector → parser → SQLite → outbox → Telegram
```

The current connector is [oppy/psg.py](oppy/psg.py).

- The first valid collection queues one summary. Long summaries travel in numbered parts with whole course blocks.
- Within a selection, Oppy matches courses by a unique source ID first, then by normalized title and venue. The course period breaks ties between otherwise identical classes.
- A failed or inconclusive collection preserves the last valid state. A missing municipality panel cannot erase the course list.
- Each change and its pending notification commit together. The outbox uses at-least-once delivery and records success after Telegram confirms receipt.
- HTTP 403, 429 or 503 ends the current cycle. Later cycles back off and honor a longer Retry-After. A successful collection restores the configured interval.

See the [parser rules](docs/psg-parser.md) and [SQLite and delivery notes](docs/offline-core.md).

## Quick start

### Requirements and installation

Use a Linux host with Git, Docker and the Docker Compose plugin. For native development, Python 3.11 or newer and system timezone data are required. The application runtime uses only the Python standard library; pytest is a development dependency.

```sh
git clone https://github.com/kayo-willian/oppy.git
cd oppy
cp -n .env.example .env
```

Keep `.env` private. Configure the Telegram credentials below. If they are left empty, monitoring can run and pending notifications remain in SQLite.

### Create the Telegram bot

1. Open a chat with `@BotFather` in Telegram. Send `/newbot`, follow the prompts and save the token.
2. Open a private chat with the new bot and send it a message.
3. In your browser, open `https://api.telegram.org/bot<TOKEN>/getUpdates`, replacing `<TOKEN>` with your token. Find the message you just sent and copy the numeric `id` inside its `chat` object.
4. Edit your local `.env` file. Set `BEACON_TELEGRAM_TOKEN` to the token and `BEACON_TELEGRAM_CHAT_ID` to the chat ID.

Treat the token like a password. Never commit or share it. The `getUpdates` URL contains the token and is saved in your browser history. If the token is exposed, revoke it with `/revoke` in BotFather.

### Run with Docker Compose

Run these commands from the repository root on Linux. The two smoke checks are optional manual operations: the portal check makes real HTTP requests and can save diagnostic snapshots if parsing fails; the Telegram check sends one real message. Confirm permission before accessing the portal. Automated tests do neither.

| Task | Command |
|---|---|
| Build the image | `docker compose build` |
| Check the portal once | `docker compose run --rm oppy python -m oppy smoke` |
| Send one test message | `docker compose run --rm oppy python -m oppy smoke-telegram` |
| Start the scheduler | `docker compose up -d` |
| Inspect the last checks and pending messages | `docker compose exec oppy python -m oppy status` |
| Read monitoring status as JSON | `docker compose exec oppy python -m oppy status --json` |
| Print the saved summary | `docker compose exec oppy python -m oppy summary` |
| Send the saved summary directly | `docker compose exec oppy python -m oppy summary --send` |
| Create a consistent SQLite backup | `docker compose exec oppy python -m oppy backup` |
| Read recent service logs | `docker compose logs --tail=50 oppy` |
| Stop the service without removing the volume | `docker compose down` |

The read-only JSON status reports last_success_utc and last_failure_utc as UTC timestamps (null until observed), pending_notifications as a count, and telegram_configured as a boolean. A missing or unreadable database produces an error on stderr and a nonzero exit.

For an existing installation, stop the previous Compose service before starting Oppy. Keep its volume when shutting down. Compose explicitly reuses `opportunity-beacon_beacon-data` across directory and project renames. Both the database and its WAL files stay under `/app/data`. Avoid `docker compose down -v`, which removes volumes. Stop any old instance before starting another: the scheduler is designed for a single worker per local database.

### Updates and backups

Before updating an existing installation, create a backup while the service is running and copy the completed file outside the container for independent storage. The backup command prints its location. Keep backups private.

```sh
docker compose exec oppy python -m oppy backup
docker compose down
git pull --ff-only origin main
docker compose up -d --build
```

Review [CHANGELOG.md](CHANGELOG.md) before updating. To restore a backup, stop the scheduler, place a copy of the saved SQLite file at a fresh path inside the mounted data volume, set `BEACON_DB_PATH` to that path, and restart. A restored database may contain pending notifications that will be delivered again. Never overwrite a database in use.

### Diagnose a changed page

When the parser rejects a listing or detail page, Oppy keeps the response bytes and a JSON file with the request URL, UTC timestamp, HTTP status, parser outcome and reason. The ten newest pairs live in owner-only directories under `failed-snapshots/` beside the database. Transport failures and oversized responses do not produce snapshots.

Run `docker compose exec oppy python -m oppy status` to find the latest HTML path. Copy its **parent directory** to retrieve both files (replace `<snapshot-id>` with the directory name reported in the path):

```sh
docker compose cp 'oppy:/app/data/failed-snapshots/<snapshot-id>' ./snapshot
```

Review the raw HTML and metadata for personal or sensitive information before sharing them publicly.

## Configuration

I kept the `BEACON_` prefix for compatibility with existing `.env` files.

| Variable | Meaning and default |
|---|---|
| `BEACON_DB_PATH` | SQLite path. Defaults to `data/beacon.sqlite3`. Keep it under the mounted data directory in Compose. |
| `BEACON_INTERVAL_MINUTES` | Minutes to wait after a completed cycle. Default 30, minimum 10; use only a frequency permitted by the source. |
| `BEACON_FAILURE_ALERT_AFTER` | Consecutive failed or inconclusive checks before one incident alert. Default 3. |
| `BEACON_NOTIFICATION_LANGUAGE` | `pt-BR` (default) or `en` (English). Applies to Telegram and the local `summary` preview. Unrecognized values fall back to Portuguese. Course titles, venues and document labels keep their source wording. |
| `BEACON_TELEGRAM_TOKEN` | Bot token from BotFather. Empty by default. |
| `BEACON_TELEGRAM_CHAT_ID` | Destination chat. If either Telegram setting is empty, notifications remain pending. |
| `BEACON_BACKUP_PATH` | New destination file. Defaults to a timestamped file beside the database. |

## Limitations

Oppy checks listings only while the machine and service are running. A short registration window can pass between checks. At-least-once delivery can produce a duplicate if the process stops after Telegram accepts a message and before SQLite records success.

Oppy is not an application submission tool. It does not inspect PDF contents; document links and labels are tracked, so replacements at an unchanged URL with an unchanged label may go undetected.

In-person registration can have an unknown status. Extraction depends on the portal’s HTML. A complete cycle requests the listing once and follows one detail link per Santarém selection, with at most one retry for eligible transient errors.

## Tests

The tests use saved HTML, temporary SQLite databases and local HTTP simulations. CI runs the offline suite. Checks against the live portal are manual.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install "pip>=25.1"
python -m pip install --group dev
python -m pytest -q
```

## Roadmap

Possible future work, not implemented or scheduled:

- Support additional public listing sources where automated access is permitted.
- Add notification channels beyond Telegram.
- Explore read-only exports.

See [open issues](https://github.com/kayo-willian/oppy/issues) for scoped proposals. Suggestions and pull requests are welcome, but a proposal is not a commitment to implementation.

## Contributing

You can help with documentation, offline regression tests, deployment feedback, data exports, notification formatting or proposals for new sources. You do not need a Telegram token, a running bot or access to the PSG portal to contribute.

1. [Fork the repository](https://github.com/kayo-willian/oppy/fork) and create a focused branch from upstream `main`.
2. Read [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md).
3. Run the offline tests, make your change and add relevant regression coverage.
4. Open a pull request against `main` and describe the actual validation and limitations.

| Resource | Purpose |
|---|---|
| [Contribution guide](CONTRIBUTING.md) | Development, review and safe testing |
| [Code of conduct](CODE_OF_CONDUCT.md) | Respectful participation |
| [Security policy](SECURITY.md) | Private vulnerability reporting options |
| [Issues](https://github.com/kayo-willian/oppy/issues) | Bug reports and feature proposals; English and Brazilian Portuguese are welcome |
| [Pull requests](https://github.com/kayo-willian/oppy/pulls) | Proposed changes and reviews |
| [Changelog](CHANGELOG.md) | Significant merged changes |

The README, contribution guide, code of conduct and security policy are available in English and Brazilian Portuguese in [pt-BR/](pt-BR/README.md). Internal technical documentation, code, commits and pull requests remain in English. Project-created public issues and issue templates use English and Brazilian Portuguese; contributors can reply or report in either language. Independent forks remain free to evolve under MIT.

## How this project was built

I came up with Oppy and defined its goals, requirements, priorities and limits. I did not write the code by hand: the implementation was done through vibe coding, with AI tools working in separate roles.

| Role | Who |
|---|---|
| Idea, requirements, decisions, testing on my own machine, reviewing and merging every pull request | Me |
| Initial project brief | ChatGPT 6 (high effort) |
| Prompt writing for each phase, review of Codex's reports, technical review of the plan | Claude Sonnet 5.5 (medium effort) |
| Code, tests and Docker setup | OpenAI Codex, GPT-6.2 Model Astra (medium effort) |

ChatGPT drafted the first brief, Claude reviewed it and suggested improvements (an outbox for notifications, hashes of normalized fields, offline tests with saved HTML, and a clear difference between a failed collection and an empty one), and I sent each phase to Codex as a prompt. Codex opened one pull request per phase. I reviewed each one, ran the Docker and smoke tests myself, and merged it only when I was satisfied. Claude did not have access to the repository and did not run the code; it worked from the reports and outputs I shared.

## License

[MIT](LICENSE).
