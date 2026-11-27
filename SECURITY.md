# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.0.x   | :white_check_mark: |

Fixes land on the latest `0.0.x` release; there are no back-ported
branches.

## Reporting a Vulnerability

If you discover a security vulnerability in `bankstatementparser-writer-qif`, report it
privately: open a
[private security advisory](https://github.com/sebastienrousseau/bankstatementparser-writer-qif/security/advisories/new)
on GitHub or email **<sebastian.rousseau@gmail.com>**. Do not open a
public issue.

Please include a description, steps to reproduce (a minimal input is
ideal, with account data redacted), the impact you see and any fix you
suggest.

## What this package does and does not protect

`bankstatementparser-writer-qif` turns transactions you already hold
into QIF text, and writes it to a path only when you call `write_qif`.

- **No network and no reads.** It opens no connection and reads no
  file; `write_qif` writes UTF-8 text to the path you give, creating
  missing parent directories.
- **One field per line.** Every line break in a value becomes a space,
  so record text cannot start a field or a record of its own (only the
  payee and memo were protected before 0.0.36).
- **No escaping beyond that.** QIF has no escape syntax; other
  characters are written as they are.
- **Amounts** that do not parse, or that are too large for 28
  significant digits at cent precision, are written as given rather
  than raising; check your input if a total matters.
- **Fuzzing.** `fuzz/fuzz_to_qif.py` drives `to_qif` with Atheris in CI
  and fails on any exception, a lost or forged record, or a line that
  does not start with a field code.

## Continuous checks

CodeQL, Bandit, `pip-audit` against the locked dependency sets, and the
Atheris fuzz target run on every pull request; OpenSSF Scorecard runs
weekly and on every push to `main`.
