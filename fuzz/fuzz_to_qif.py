# SPDX-FileCopyrightText: 2026 Sebastien Rousseau <sebastian.rousseau@gmail.com>
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Coverage-guided Atheris fuzz target for the QIF writer.

``to_qif`` takes records from a parsed statement (dicts here, the most
permissive input it accepts) whose amounts, dates and text come from
whatever bank produced the file. QIF is line-based: each line is one
field, its first character the field code, and ``^`` ends a record. So
whatever a record holds, the document must keep that shape:

* ``to_qif`` never raises;
* there is exactly one ``^`` line per record;
* every other line after the header starts with a field code the
  writer emits (``D``, ``T``, ``P``, ``M``, ``N``, ``L``), so record
  text can never start a field or a record of its own.

Any exception, or a broken invariant, escapes the target and libFuzzer
records it as a crash.

Run (Linux x86_64, Python 3.12+, ``poetry install --with fuzz``)::

    python fuzz/fuzz_to_qif.py fuzz/corpus -max_total_time=60
"""

from __future__ import annotations

import sys

import atheris

with atheris.instrument_imports():
    from bankstatementparser_writer_qif import to_qif

_FIELDS = (
    "amount",
    "date",
    "payee",
    "description",
    "memo",
    "reference",
    "check_number",
    "category",
)
_CODES = ("D", "T", "P", "M", "N", "L")


def _records(fdp: atheris.FuzzedDataProvider) -> list[dict[str, str]]:
    """Build up to four records whose fields are fuzzed strings."""
    records = []
    for _ in range(fdp.ConsumeIntInRange(0, 4)):
        records.append(
            {
                name: fdp.ConsumeUnicodeNoSurrogates(24)
                for name in _FIELDS
                if fdp.ConsumeBool()
            }
        )
    return records


def _check(qif: str, count: int) -> None:
    """Fail unless ``qif`` holds ``count`` well-formed records."""
    header, *lines = qif.split("\n")
    if header != "!Type:Bank" or lines[-1] != "":
        raise AssertionError(f"bad framing {header!r} ... {lines[-1:]!r}")
    lines = lines[:-1]
    if lines.count("^") != count:
        raise AssertionError(f"{lines.count('^')} records, {count} given")
    for line in lines:
        if line != "^" and (len(line) < 2 or line[0] not in _CODES):
            raise AssertionError(f"stray line {line!r}")


def test_one_input(data: bytes) -> None:
    """Write one fuzzed batch of records and check the document."""
    fdp = atheris.FuzzedDataProvider(data)
    records = _records(fdp)
    _check(to_qif(records), len(records))


def main() -> None:
    """Hand the target to libFuzzer with the command-line options."""
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
