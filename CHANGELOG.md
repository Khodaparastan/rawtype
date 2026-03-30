# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [Unreleased]

## [0.1.1] - 2026-03-30
### Added
- Changelog housekeeping for release process clarity.
- Script entry point in pyproject.toml.
- poetry lock file.

### Changed
- Minor documentation clarifications in `README.md`.

## [0.1.0] - 2026-03-30
### Added
- Initial release of `rawtype`, a macOS keyboard typing automation tool that simulates hardware keystrokes using AppleScript keycodes.
- CLI commands:
  - `rawtype text "..."` — type a provided string.
  - `rawtype file <path>` — type contents of a file (chunked to avoid AppleScript memory limits).
  - `rawtype stdin` — type content piped from standard input.
  - `rawtype test` — run a keyboard mapping test.
- Options: `--delay`, `--wait`, `--verbose`, `--chunk-size` (file mode only).
- Default ANSI (US) keymap with graceful skipping of unmapped characters (reportable via `--verbose`).

<!--
Reference links (fill in when repository hosting is available):
[Unreleased]: https://github.com/khodaparastan/rawtype/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/khodaparastan/rawtype/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/khodaparastan/rawtype/releases/tag/v0.1.0
-->
