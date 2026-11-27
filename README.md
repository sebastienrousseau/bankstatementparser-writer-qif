<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

<p align="center">
  <img src="https://cloudcdn.pro/bankstatementparser/v1/logos/bankstatementparser.svg" alt="bankstatementparser-writer-qif logo" width="128" />
</p>

<h1 align="center">bankstatementparser-writer-qif</h1>

<p align="center">
  Writes bankstatementparser transactions as Quicken Interchange Format (QIF) files for GnuCash, Moneydance, Quicken, YNAB and other accounting tools.
</p>

<p align="center">
  <a href="https://github.com/sebastienrousseau/bankstatementparser-writer-qif/actions"><img src="https://img.shields.io/github/actions/workflow/status/sebastienrousseau/bankstatementparser-writer-qif/ci.yml?style=for-the-badge&logo=github" alt="Build" height="28" /></a>
  <a href="https://pypi.org/project/bankstatementparser-writer-qif/"><img src="https://img.shields.io/pypi/v/bankstatementparser-writer-qif?style=for-the-badge&color=fc8d62&logo=python" alt="Registry" height="28" /></a>
  <a href="https://sebastienrousseau.com/bankstatementparser-writer-qif/"><img src="https://img.shields.io/badge/docs-user%20manual-0a7bbb?style=for-the-badge&labelColor=555555&logo=materialformkdocs" alt="Docs" height="28" /></a>
  <a href="https://scorecard.dev/viewer/?uri=github.com/sebastienrousseau/bankstatementparser-writer-qif"><img src="https://img.shields.io/ossf-scorecard/github.com/sebastienrousseau/bankstatementparser-writer-qif?style=for-the-badge&label=OpenSSF%20Scorecard&logo=openssf" alt="OpenSSF Scorecard" height="28" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0%20OR%20MIT-blue.svg?style=for-the-badge" alt="License: Apache-2.0 OR MIT" height="28" /></a>
  <a href="https://github.com/sebastienrousseau/bankstatementparser-writer-qif/blob/main/docs/POLICIES.md"><img src="https://img.shields.io/badge/python-3.10%2B-93450a.svg?style=for-the-badge&logo=python" alt="Python 3.10+" height="28" /></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/sebastienrousseau/bankstatementparser-writer-qif/main/.github/demo.gif" alt="A terminal printing the installed version, 0.0.36, then the two examples: two transactions written as QIF with ISO and US dates, and a CSV statement converted to a four-record QIF file" width="100%" />
</p>

---

## Contents

**Getting started**

- [Install](#install): PyPI, source
- [Requirements](#requirements): toolchain floor, platforms
- [Quick Start](#quick-start): convert a parsed statement to QIF

**The bankstatementparser-writer-qif ecosystem**

- [The bankstatementparser-writer-qif ecosystem](#the-bankstatementparser-writer-qif-ecosystem): the core library, the loaders, writers and servers

**Library reference**

- [Capabilities at a glance](#capabilities-at-a-glance): the current surface by theme
- [Ecosystem comparison](#ecosystem-comparison): short matrix; full table at [`docs/COMPARISON.md`](docs/COMPARISON.md)
- [Benchmarks](#benchmarks): headline numbers; full table at [`docs/BENCHMARKS.md`](docs/BENCHMARKS.md)
- [Features](#features): the public API and field mapping
- [Configuration](#configuration): the writer's arguments
- [Examples](#examples): runnable example index

**Operational**

- [When not to use bankstatementparser-writer-qif](#when-not-to-use-bankstatementparser-writer-qif): limitations
- [Development](#development): make targets, fuzzing, CI
- [Security](#security): guarantees and compliance
- [Documentation](#documentation): all reference docs
- [Stability guarantees](#stability-guarantees): SemVer axis, output stability, minimum toolchain discipline
- [License](#license)

---

## Install

### As a Python library

```bash
pip install bankstatementparser-writer-qif
```

That installs the writer, `bankstatementparser >= 0.0.35` and pandas.

| Channel | Command | Notes |
| :--- | :--- | :--- |
| PyPI | `pip install bankstatementparser-writer-qif` | Pulls in `bankstatementparser >= 0.0.35` |
| Source | `git clone https://github.com/sebastienrousseau/bankstatementparser-writer-qif && cd bankstatementparser-writer-qif && poetry install` | For local development |

Verify the installation:

```sh
python -c "import bankstatementparser_writer_qif as w; print(w.__version__)"
# -> 0.0.36
```

An isolated virtual environment keeps its dependencies apart:

```sh
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
python -m pip install -U bankstatementparser-writer-qif
```

---

## Requirements

- **Python 3.10 or later.** CI tests CPython 3.10, 3.11, 3.12, 3.13 and 3.14 on Linux, macOS and Windows; [`docs/POLICIES.md`](docs/POLICIES.md) says when the floor moves.
- **[`bankstatementparser`](https://pypi.org/project/bankstatementparser/) 0.0.35 or later**, for the `Transaction` model and the parsers that feed the writer, and pandas, which it brings.

---

## Quick Start

```python
from bankstatementparser import create_parser

from bankstatementparser_writer_qif import write_qif

# 1. Parse any statement the core supports (e.g. CAMT.053, MT940, CSV)
parser = create_parser("statement.xml")

# 2. Write it as a QIF file
write_qif(parser, "statement_export.qif", account_type="Bank")
```

`write_qif` accepts the parser itself (it calls `parse()`), the DataFrame `parse()` returns, a list of `Transaction` objects or a list of dicts, and returns the `Path` it wrote. `to_qif` takes the same arguments without the destination and returns the text.

---

## The bankstatementparser-writer-qif ecosystem

`bankstatementparser` is a modular suite whose packages ship one version together. This package is its QIF writer; the full table, with every loader, writer and server, is in [The suite](docs/suite.md).

| Component | Purpose | Use case |
| :--- | :--- | :--- |
| [`bankstatementparser`](https://github.com/sebastienrousseau/bankstatementparser) | The parser core: CAMT, pain.001, CSV, OFX, QFX, MT940 and PDF statements | Parsing statements from Python or the CLI |
| **`bankstatementparser-writer-qif`** | Transactions to QIF | Importing statements into accounting tools |
| Other writers | XLSX, OFX and SWIFT MT940/MT942 | Other export formats |
| Loaders | BAI2, MT942, CFONB, CAMT.054, SEPA and BACS | Formats beyond the core |
| [`bankstatementparser-transport-ebics`](https://github.com/sebastienrousseau/bankstatementparser-transport-ebics), [`bankstatementparser-mcp`](https://github.com/sebastienrousseau/bankstatementparser-mcp), [`bankstatementparser-lsp`](https://github.com/sebastienrousseau/bankstatementparser-lsp) | EBICS data, Model Context Protocol and Language Server Protocol | Bank downloads, AI agents and editors |

---

## Capabilities at a glance

| Area | Capability | Status |
| :--- | :--- | :--- |
| Input | `list[Transaction]`, `pandas.DataFrame`, `list[dict]`, or a core parser object | Shipped |
| Header | `!Type:Bank` by default; any account type as given (`CCard`, `Cash`, ...) | Shipped |
| Fields | `D` (date), `T` (amount), `P` (payee), `M` (memo), `N` (reference or check number), `L` (category), `^` (end) | Shipped |
| Dates | ISO `YYYY-MM-DD` by default, or any `strftime` format such as `%m/%d/%Y` | Shipped |
| Line safety | Every line break in a value becomes a space | Shipped |
| Investments, splits, accounts | `!Type:Invst` fields, split lines, `!Account` blocks | Not implemented |

---

## Ecosystem comparison

The choice is between this one-call writer for parsed statements and a full QIF library. Every cell comes from this repository or the other project's PyPI description.

| Project | Writes QIF | Reads QIF | Writes from |
| :--- | :---: | :---: | :---: |
| **bankstatementparser-writer-qif** | Yes | No | `bankstatementparser` transactions |
| [`quiffen`](https://pypi.org/project/quiffen/) | Yes | Yes | Its own QIF object model |

See [`docs/COMPARISON.md`](docs/COMPARISON.md) for the evidence and complete matrix.

---

## Benchmarks

`benches/bench_to_qif.py` times one `to_qif` call for each input shape as the statement grows. Cost is linear: about 3 us per transaction from dicts or `Transaction` objects and 17 us from a DataFrame.

| Scenario | Result | Environment |
| :--- | ---: | :--- |
| 1,000 `Transaction` objects | 3.1 ms | Apple M1 Pro, macOS 27.2.1, CPython 3.12.16 |
| 10,000 `Transaction` objects (521 KiB of QIF) | 33 ms | Apple M1 Pro, macOS 27.2.1, CPython 3.12.16 |
| 10,000-row DataFrame | 166 ms | Apple M1 Pro, macOS 27.2.1, CPython 3.12.16 |

See [`docs/BENCHMARKS.md`](docs/BENCHMARKS.md) for methodology and full results.

---

## Features

- `to_qif(data, account_type="Bank", date_format="%Y-%m-%d") -> str`: serialises transactions to QIF text.
- `write_qif(data, destination, account_type="Bank", date_format="%Y-%m-%d") -> Path`: writes that text to `destination` as UTF-8, creating missing parent directories.

Each record becomes a `D` line from the date, `T` from the amount (two decimals), `P` from the payee or description, `M` from the memo, `N` from the reference or check number and `L` from the category, then `^`; an empty field is left out. The [Usage](docs/usage.md) page has the full mapping and fallbacks.

---

## Configuration

There is no configuration file or environment variable; the writer's arguments are the configuration:

| Argument | Default | Meaning |
| :--- | :--- | :--- |
| `account_type` | `"Bank"` | The header, `!Type:<account_type>` |
| `date_format` | `"%Y-%m-%d"` | The `strftime` format for `D` lines; `"%m/%d/%Y"` for Quicken |

---

## Examples

[`examples/`](examples/) holds two runnable scripts, each run in CI:

| Example | Demonstrates |
| :--- | :--- |
| [`01_basic_usage.py`](examples/01_basic_usage.py) | Two `Transaction` objects written with `to_qif`, with ISO and with US dates |
| [`02_advanced_workflow.py`](examples/02_advanced_workflow.py) | A CSV statement ([`examples/data/statement.csv`](examples/data/statement.csv)) converted to a QIF file with `write_qif` |

---

## When not to use bankstatementparser-writer-qif

- **You need investment accounts, splits or several accounts in one file.** Records are bank-style (`D`, `T`, `P`, `M`, `N`, `L`); there are no `!Type:Invst` fields, split lines or `!Account` blocks.
- **You need currencies.** QIF has no currency field; amounts are numbers only.
- **You need bad input reported.** An amount that does not parse, or is too large to write with cents, is written as given, and empty fields are left out, without an error.
- **You need to read QIF.** This package only writes it.

---

## Development

```bash
git clone https://github.com/sebastienrousseau/bankstatementparser-writer-qif.git
cd bankstatementparser-writer-qif
poetry install
make check
```

`make check` runs the local gates: `ruff` lint and format, `mypy --strict`, Bandit, the complexity baseline (`scripts/check_complexity.py`), `pytest` with a 100% line and branch coverage floor, `interrogate` at 100% docstring coverage, the examples and the README template check. Other targets: `make bench`, `make fuzz` (Atheris, 60 s, Linux x86_64 with Python 3.12+), `make docs` (the MkDocs manual, `--strict`), `make audit` (`pip-audit` on the locked sets) and `make demo` (re-renders the GIF above with VHS from `.github/demo.tape`). CI adds the OS by Python matrix, the fuzz job, CodeQL and the Docs Lint gates. [`CONTRIBUTING.md`](CONTRIBUTING.md) covers the workflow and commit rules.

---

## Security

- **No network and no reads.** The writer opens no connection and reads no file; `write_qif` writes only to the path you give.
- **One field per line.** Every line break in a value becomes a space, so record text cannot start a field or a record of its own. QIF has no escape syntax, so nothing else is changed.
- **Fuzzing.** `fuzz/fuzz_to_qif.py` drives `to_qif` with Atheris in CI and fails on any exception, a lost or forged record, or a line without a field code. It found the line breaks fixed in 0.0.36.
- **Supply chain.** Dependencies are locked in `poetry.lock`, CI installs hash-pinned exports of it, and `pip-audit`, Bandit and CodeQL run on every change. Releases publish to PyPI through OIDC trusted publishing and carry cosign signatures, SLSA provenance and SBOMs; every workflow action is pinned by commit SHA except the SLSA generator, which must be referenced by tag.

Report vulnerabilities according to [`SECURITY.md`](SECURITY.md).

---

## Documentation

- **User manual:** [sebastienrousseau.com/bankstatementparser-writer-qif](https://sebastienrousseau.com/bankstatementparser-writer-qif/), built from [`docs/`](docs/) with MkDocs
- **API reference:** [the manual's API page](https://sebastienrousseau.com/bankstatementparser-writer-qif/api/), generated from the docstrings
- **Developer docs:** [`CONTRIBUTING.md`](CONTRIBUTING.md), [`ARCHITECTURE.md`](ARCHITECTURE.md), [`GOVERNANCE.md`](GOVERNANCE.md), [`SUPPORT.md`](SUPPORT.md)
- **The suite:** [`docs/suite.md`](docs/suite.md), with every `bankstatementparser` package
- **History:** [`CHANGELOG.md`](CHANGELOG.md)

---

## Stability guarantees

- **Versioning.** Releases stay on the `0.0.x` line and step by exactly `0.0.1`, in lockstep with the rest of the `bankstatementparser` suite. Under SemVer a `0.0.x` release may break anything; this project names each break in the CHANGELOG instead.
- **The breaking axis is the output**: the QIF the writer produces for a given input. A change to a line, its value or its fallback is called out in the CHANGELOG as breaking, even when no Python signature moves.
- **Python API.** `to_qif` and `write_qif` keep their names and arguments; names starting with `_` are internal.
- **Minimum toolchain.** Python 3.10 is the floor; it moves only in a release, for the whole suite at once, with the reason in the CHANGELOG ([`docs/POLICIES.md`](docs/POLICIES.md)).

---

## License

Dual-licensed under [Apache License, Version 2.0](LICENSE-APACHE) or [MIT](LICENSE-MIT), at your option (`SPDX-License-Identifier: Apache-2.0 OR MIT`). Any contribution submitted for inclusion in the work shall be dual-licensed as above, without additional terms or conditions.
