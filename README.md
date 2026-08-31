# Quicken Interchange Format (QIF) Writer for Bank Statement Parser

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0_OR_MIT-blue.svg)](LICENSE)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/sebastienrousseau/bankstatementparser-writer-qif)

Quicken Interchange Format (QIF) export writer plugin for [`bankstatementparser`](https://github.com/sebastienrousseau/bankstatementparser).

---

## Features

- **Standard QIF Serialization**: Generates clean, compliant QIF files compatible with Quicken, GnuCash, Ledger, Money, and standard accounting software.
- **Multiple Input Shapes**: Seamlessly accepts `list[Transaction]`, `pandas.DataFrame`, `list[dict]`, or any `bankstatementparser` statement parser object.
- **Configurable Formats**: Customize account type header (`Bank`, `CCard`, `Cash`, `Invst`) and date format string (`%Y-%m-%d`, `%d/%m/%Y`, `%m/%d/%Y`).
- **100% Type Safe & Tested**: Full static typing and 100% test coverage.

---

## Installation

```bash
pip install bankstatementparser-writer-qif
```

---

## Quickstart

```python
from bankstatementparser.transaction_models import Transaction
from bankstatementparser_writer_qif import write_qif
from decimal import Decimal
from datetime import date

transactions = [
    Transaction(
        account_id="FR7612345",
        amount=Decimal("1500.50"),
        booking_date=date(2026, 1, 15),
        description="Salary Payment",
        reference="SAL-001",
        category="Income:Salary",
    ),
    Transaction(
        account_id="FR7612345",
        amount=Decimal("-45.20"),
        booking_date=date(2026, 1, 16),
        description="Coffee Shop",
        reference="TX9988",
        category="Expenses:Dining",
    ),
]

# Write to QIF file
write_qif(transactions, "statement.qif")
```

---

## License

Dual-licensed under Apache 2.0 and MIT.
