<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# bankstatementparser-writer-qif Architecture

A map of the codebase for contributors. The package is one module of
pure functions; the only I/O is `write_qif` writing the finished text.

## The flow

```text
list[Transaction] | DataFrame | list[dict] | core parser
        |
        v
_normalize_records()                 -> list[dict]
        |
        v  per record
_record_lines(rec, date_format)
        _coerce_date_str()           D line
        _coerce_amount_str()         T line (two decimals, or as given)
        payee / memo / reference / category -> P, M, N, L lines
        _one_line()                  every line break becomes a space
        "^"
        v
to_qif(): "!Type:<account_type>" + lines   -> str
write_qif(): to_qif() -> UTF-8 file        -> Path
```

## Module map

| Area | Path | Responsibility |
| :--- | :--- | :--- |
| **Writer** | `bankstatementparser_writer_qif/writer.py` | Input normalisation, field formatting, `to_qif`, `write_qif` |
| **Version** | `bankstatementparser_writer_qif/__init__.py` | `__version__` and the public re-exports |
| **Tests** | `tests/` | Writer behaviour (including Hypothesis properties), concurrency and stress, examples, release notes and the suite's vendored conformance checks; 100% line and branch coverage |
| **Fuzzing** | `fuzz/fuzz_to_qif.py`, `fuzz/corpus/` | Atheris target for `to_qif`, run by the CI `Fuzz (Atheris)` job |
| **Benchmarks** | `benches/bench_to_qif.py` | `to_qif` cost by input shape and size |
| **Examples** | `examples/`, `examples/data/` | Transactions to QIF, and a CSV-to-QIF conversion |
| **Manual** | `mkdocs.yml`, `docs/` | MkDocs Material user manual and API reference, deployed to GitHub Pages |
| **Release helpers** | `scripts/` | `verify_versions.py`, `release_notes.py`, `export_locked_requirements.py` (hashed exports of `poetry.lock` into `requirements/`), `check_complexity.py`, `check_suite_consistency.py`, `readme-check.sh` |

## Design decisions

- **One normalised shape.** Every input becomes a list of dicts first,
  so the formatting code has one path whatever the caller passed.
- **One field per line.** QIF has no escaping, so the only protection a
  writer can give is to keep each value on its line; `_one_line` does
  that for every field and the fuzz target checks it.
- **Never raise on a bad value.** An amount that does not parse, or is
  too large to write with cents, is written as given, and an empty
  field is left out, so one odd row cannot abort an export.

## CI

`ci.yml` runs the tests on ubuntu, macOS and Windows with CPython 3.10
to 3.14, plus lint, types, Bandit, the complexity baseline, the
examples, the fuzz target and a wheel smoke test. `docs.yml` builds the
manual with `--strict`; `docs-lint.yml` checks the README template and
Markdown; `security.yml` runs `pip-audit`; `codeql.yml` and
`scorecard.yml` scan; `release.yml` publishes a tag.
