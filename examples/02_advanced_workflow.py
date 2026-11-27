# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Convert a CSV statement to a QIF file.

Parses ``examples/data/statement.csv`` with the core
``bankstatementparser``, writes it with ``write_qif`` to a temporary
directory, and prints the file and a per-record summary read back from
its ``T`` (amount) and ``P`` (payee) lines.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from bankstatementparser import create_parser

from bankstatementparser_writer_qif import write_qif

DATA = Path(__file__).resolve().parent / "data"


def main() -> None:
    """CSV in, QIF out."""
    parser = create_parser(str(DATA / "statement.csv"))
    with tempfile.TemporaryDirectory() as tmp:
        target = write_qif(parser, Path(tmp) / "statement.qif")
        text = target.read_text(encoding="utf-8")
    records = text.split("^\n")[:-1]
    print(f"Wrote {target.name}: {len(records)} records, {len(text)} bytes")
    total = 0.0
    for record in records:
        fields = {line[0]: line[1:] for line in record.splitlines()}
        total += float(fields["T"])
        print(f"  {fields['D']}  {fields['T']:>9}  {fields['P']}")
    print(f"Net movement: {total:.2f}")


if __name__ == "__main__":
    main()
