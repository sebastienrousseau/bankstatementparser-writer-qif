# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Serialise Transaction objects to QIF.

Builds two ``bankstatementparser`` transactions and prints the QIF
``to_qif`` writes for them, first with ISO dates and then with the
US ``MM/DD/YYYY`` dates Quicken expects.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from bankstatementparser.transaction_models import Transaction

from bankstatementparser_writer_qif import to_qif


def main() -> None:
    """Write two transactions in both date formats."""
    transactions = [
        Transaction(
            account_id="ACC-001",
            amount=Decimal("150.00"),
            currency="EUR",
            booking_date=date(2026, 1, 15),
            description="Invoice 1024",
            reference="E2E-001",
            category="Income:Consulting",
        ),
        Transaction(
            account_id="ACC-001",
            amount=Decimal("-42.50"),
            currency="EUR",
            booking_date=date(2026, 1, 16),
            description="Card payment",
            reference="CARD-0116",
        ),
    ]
    print(to_qif(transactions), end="")
    print("--- with date_format='%m/%d/%Y' and account_type='CCard':")
    print(
        to_qif(transactions, account_type="CCard", date_format="%m/%d/%Y"),
        end="",
    )


if __name__ == "__main__":
    main()
