# Contributing to Oppy

[Português (Brasil)](pt-BR/CONTRIBUICAO.md)

Contributions are welcome, whether you are learning Python, Linux or Docker or already maintain monitoring software. Oppy is a small, independent self-hosted project. You can fork it, report a problem, improve the documentation or submit a focused pull request. These guidelines apply to upstream contributions, not independent forks under the [MIT license](LICENSE).

## Scope

Oppy monitors public opportunity listings and sends notifications. Its only implemented source is Senac Pará PSG for free courses in Santarém. Telegram is the only implemented external notification provider. Keep the monitoring core simple, preserve the existing behavior and discuss new sources, dependencies or significant architectural changes in an issue first.

Useful contributions include reproducible bugs, fixture-based regression tests, accessibility and notification formatting, installation documentation, read-only exports and well-scoped source proposals.

See the [GitHub contributors list](https://github.com/kayo-willian/oppy/graphs/contributors) for commit credits.

## Getting started

Use a Linux development environment with Git and Python 3.11 or newer. The runtime uses the standard library. The offline tests need pytest, but do not need Docker, a Telegram account, credentials or live access to the portal.

1. Fork the repository on GitHub and clone your fork.
2. Add the upstream remote and create a topic branch.

   ```sh
   git clone https://github.com/YOUR-USERNAME/oppy.git
   cd oppy
   git remote add upstream https://github.com/kayo-willian/oppy.git
   git fetch upstream
   git switch -c fix/descriptive-name upstream/main
   ```

3. Prepare the development environment and run the existing suite.

   ```sh
   python3 -m venv .venv
   . .venv/bin/activate
   python -m pip install "pip>=25.1"
   python -m pip install --group dev
   python -m pytest -q
   ```

4. Make the smallest coherent change. Add regression tests where appropriate. Rerun the suite and check the diff.
5. Commit and push to your fork, then open a pull request targeting upstream `main`.

   ```sh
   git diff --check
   git status --short
   git add -- path/to/changed-file
   git commit -m "fix: describe the change"
   git push -u origin fix/descriptive-name
   ```

Replace the example username, branch and file path. Use descriptive branch names and keep unrelated changes separate.

## Technical and safety requirements

- Keep automated tests offline. Use reduced, sanitized HTML fixtures, temporary SQLite databases, mocked providers and loopback simulations. Do not contact the real PSG portal or send Telegram messages in pytest or CI.
- Confirm applicable access conditions before proposing or manually testing a live source. Use an identifiable User-Agent, bounded requests, conservative intervals and Retry-After handling. Never bypass access controls, CAPTCHA or rate limits, guess identifiers or collect applicant data.
- Keep source-specific parsing separate from normalized records and change detection. Preserve stable course identities, unknown states and the last valid collection. An empty or malformed response must not erase valid data.
- Preserve atomic state/event/outbox writes, event deduplication and at-least-once delivery. Do not claim exactly-once Telegram delivery.
- Preserve existing `BEACON_` settings, database migrations and the legacy Compose volume name unless an explicit compatibility plan is reviewed.
- Keep credentials, real environment files, SQLite databases, private logs and raw failed HTML snapshots out of Git and public reports. Sanitize fixtures before adding them.
- Prefer the existing standard-library architecture. Do not add services, databases or dependencies without a clear need.

Read [parser notes](docs/psg-parser.md), [source reconnaissance](docs/psg-recon.md) and [core documentation](docs/offline-core.md) for implementation context.

## Issues and proposals

Search existing issues and PRs before opening a new one. Use the bug report or feature proposal template. Include the commit, environment, reproduction steps, expected and actual behavior, and sanitized evidence. A source proposal should identify the public listing, access conditions, identity fields, expected changes and a safe offline test plan; do not implement or run recurring collection before review.

Public issues and issue templates are bilingual (English and Brazilian Portuguese). You may write a report or reply in either language; translating it yourself is not required. Code, commits and pull requests use English. Translations of technical and community documents live in `pt-BR/` and should stay aligned with the English originals. For suspected vulnerabilities, follow [SECURITY.md](SECURITY.md) rather than posting sensitive details publicly.

## Review checklist

Explain the problem, scope, compatibility impact and tradeoffs. Report tests actually run, including failures and checks not performed. Update documentation and the Unreleased section of [CHANGELOG.md](CHANGELOG.md) for significant user-visible changes. For documentation-only work, verify links, commands, technical accuracy and the diff.

Disclose material AI assistance in your PR, verify the changes yourself and credit external work and its license. Submit only material you have the right to contribute under MIT. Do not invent authorship, validation results or source permission.

Pull requests are reviewed before merge. Proposals may be declined or deferred; there is no promised response time or release schedule. Follow the [code of conduct](CODE_OF_CONDUCT.md).
