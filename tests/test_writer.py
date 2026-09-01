# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Tests for Quicken Interchange Format (QIF) Writer."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import pandas as pd
from bankstatementparser.transaction_models import Transaction
from hypothesis import given
from hypothesis import strategies as st

from bankstatementparser_writer_qif import __version__, to_qif, write_qif
from bankstatementparser_writer_qif.writer import (
    _coerce_amount_str,
    _coerce_date_str,
    _normalize_records,
)


class DummyParserWithTransactions:
    """Mock parser implementing to_transactions."""

    def to_transactions(self) -> list[Transaction]:
        """Return dummy transactions."""
        return [
            Transaction(
                account_id="ACC01",
                amount=Decimal("120.00"),
                booking_date=date(2026, 1, 1),
                description="Dummy Parser Tx",
            )
        ]


class DummyParserWithDataFrame:
    """Mock parser implementing parse."""

    def parse(self) -> pd.DataFrame:
        """Return dummy DataFrame."""
        return pd.DataFrame(
            [
                {
                    "date": "2026-01-02",
                    "amount": 250.50,
                    "description": "DF Parser Tx",
                }
            ]
        )


def test_version() -> None:
    """Verifies that version is exposed and semantic."""
    assert __version__ == "0.0.19"


def test_to_qif_with_transactions() -> None:
    """Tests QIF output from Transaction domain models."""
    txs = [
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
            description="Coffee Shop\nDowntown",
            reference="TX9988",
            category="Expenses:Dining",
        ),
    ]

    out = to_qif(txs, account_type="Bank", date_format="%Y-%m-%d")

    assert "!Type:Bank" in out
    assert "D2026-01-15" in out
    assert "T1500.50" in out
    assert "PSalary Payment" in out
    assert "MSAL-001" in out
    assert "NSAL-001" in out
    assert "LIncome:Salary" in out
    assert "PCoffee Shop Downtown" in out
    assert "T-45.20" in out
    assert out.count("^") == 2


def test_to_qif_with_dataframe() -> None:
    """Tests QIF output from pandas DataFrame."""
    df = pd.DataFrame(
        [
            {
                "date": "2026-01-20",
                "amount": 300.00,
                "payee": "Client Invoice",
                "memo": "INV-1001",
                "reference": "REF1001",
                "category": "Revenue",
            }
        ]
    )

    out = to_qif(df, account_type="CCard", date_format="%d/%m/%Y")
    assert "!Type:CCard" in out
    assert "D20/01/2026" in out
    assert "T300.00" in out
    assert "PClient Invoice" in out
    assert "MINV-1001" in out
    assert "NREF1001" in out
    assert "LRevenue" in out


def test_to_qif_with_dict_records() -> None:
    """Tests QIF output from dictionary rows."""
    records = [
        {
            "booking_date": datetime(2026, 1, 25, 12, 0, 0),
            "amount": "-1,250.75",
            "description": "Monthly Rent",
            "extra_info": "Apartment 4B",
            "check_number": "CHK-555",
        }
    ]
    out = to_qif(records)
    assert "D2026-01-25" in out
    assert "T-1250.75" in out
    assert "PMonthly Rent" in out
    assert "MApartment 4B" in out
    assert "NCHK-555" in out


def test_write_qif_file(tmp_path: Path) -> None:
    """Tests writing QIF output to disk."""
    dest = tmp_path / "subdir" / "export.qif"
    txs = [
        Transaction(
            account_id="ACC99",
            amount=Decimal("50.00"),
            booking_date=date(2026, 2, 1),
            description="Bookstore",
        )
    ]
    path = write_qif(txs, dest)
    assert path.exists()
    assert "!Type:Bank" in path.read_text(encoding="utf-8")


def test_dummy_parsers() -> None:
    """Tests parser object duck typing in _normalize_records."""
    p1 = DummyParserWithTransactions()
    r1 = _normalize_records(p1)
    assert len(r1) == 1
    assert r1[0]["payee"] == "Dummy Parser Tx"

    p2 = DummyParserWithDataFrame()
    r2 = _normalize_records(p2)
    assert len(r2) == 1
    assert r2[0]["description"] == "DF Parser Tx"


def test_coercion_edge_cases() -> None:
    """Tests date and amount coercion edge cases."""
    assert _coerce_date_str(None) is None
    assert _coerce_date_str(float("nan")) is None
    assert _coerce_date_str("") is None
    assert _coerce_date_str("   ") is None
    assert _coerce_date_str("2026-99-99") == "2026-99-99"
    assert _coerce_date_str("non-iso-date-string") == "non-iso-date-string"
    assert _coerce_date_str(12345) == "12345"

    assert _coerce_amount_str(None) is None
    assert _coerce_amount_str(float("nan")) is None
    assert _coerce_amount_str("") is None
    assert _coerce_amount_str("   ") is None
    assert _coerce_amount_str("not-a-number") == "not-a-number"
    assert _coerce_amount_str(42) == "42.00"
    assert _coerce_amount_str([100]) == "[100]"


@given(
    amount=st.decimals(
        min_value=Decimal("-999999.99"),
        max_value=Decimal("999999.99"),
        places=2,
    ),
    payee=st.text(min_size=1, max_size=30).filter(lambda s: "\x00" not in s),
)
def test_fuzz_to_qif(amount: Decimal, payee: str) -> None:
    """Property-based fuzzing of to_qif generation."""
    txs = [
        Transaction(
            account_id="FUZZ_ACC",
            amount=amount,
            booking_date=date(2026, 1, 1),
            description=payee,
        )
    ]
    out = to_qif(txs)
    assert "!Type:Bank" in out
    assert "^" in out
