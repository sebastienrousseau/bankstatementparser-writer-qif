# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Structured Quicken Interchange Format (QIF) Writer."""

from __future__ import annotations

import os
from collections.abc import Mapping, Sequence
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import pandas as pd
from bankstatementparser.transaction_models import Transaction

__all__ = ["to_qif", "write_qif"]


def _coerce_date_str(val: Any, date_format: str = "%Y-%m-%d") -> str | None:
    """Coerce various date types to formatted string."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    if isinstance(val, (date, datetime)):
        return val.strftime(date_format)
    if isinstance(val, str):
        clean = val.strip()
        if not clean:
            return None
        # Try ISO format parse first
        if len(clean) >= 10 and clean[4] == "-" and clean[7] == "-":
            try:
                dt = date.fromisoformat(clean[:10])
                return dt.strftime(date_format)
            except ValueError:
                return clean
        return clean
    return str(val)


def _coerce_amount_str(val: Any) -> str | None:
    """Coerce amount values to decimal string with 2 decimal places."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    if isinstance(val, (Decimal, int, float)):
        return f"{val:.2f}"
    if isinstance(val, str):
        clean = val.strip().replace(",", "")
        if not clean:
            return None
        try:
            d = Decimal(clean)
            return f"{d:.2f}"
        except Exception:
            return clean
    return str(val)


def _normalize_records(
    data: (
        Sequence[Transaction]
        | pd.DataFrame
        | Sequence[Mapping[str, Any]]
        | Any
    ),
) -> list[dict[str, Any]]:
    """Normalize supported data inputs into standard dictionary rows."""
    data_any: Any = data
    if hasattr(data_any, "to_transactions") and callable(
        data_any.to_transactions
    ):
        txs = data_any.to_transactions()
        return _normalize_records(txs)

    if hasattr(data_any, "parse") and callable(data_any.parse):
        df = data_any.parse()
        return _normalize_records(df)

    if isinstance(data, pd.DataFrame):
        records = []
        for _, row in data.iterrows():
            rec = row.to_dict()
            records.append(rec)
        return records

    records = []
    for item in data:
        if isinstance(item, Transaction):
            records.append(
                {
                    "date": item.booking_date or item.value_date,
                    "amount": item.amount,
                    "payee": item.description,
                    "memo": item.reference or item.transaction_id,
                    "reference": item.reference,
                    "category": item.category,
                }
            )
        elif isinstance(item, Mapping):
            records.append(dict(item))
    return records


def to_qif(
    data: (
        Sequence[Transaction]
        | pd.DataFrame
        | Sequence[Mapping[str, Any]]
        | Any
    ),
    account_type: str = "Bank",
    date_format: str = "%Y-%m-%d",
) -> str:
    """Serialise bank transactions to a Quicken Interchange Format (QIF) text string.

    Args:
        data: Transactions as DataFrame, Transaction list, or dict records.
        account_type: QIF header type (default 'Bank', e.g. 'Bank', 'CCard', 'Cash').
        date_format: Date format string for 'D' fields (default '%Y-%m-%d').

    Returns:
        Formatted QIF string.
    """
    records = _normalize_records(data)
    lines: list[str] = [f"!Type:{account_type}"]

    for rec in records:
        # Date
        d_val = (
            rec.get("date") or rec.get("booking_date") or rec.get("value_date")
        )
        d_str = _coerce_date_str(d_val, date_format)
        if d_str:
            lines.append(f"D{d_str}")

        # Amount
        amt_val = rec.get("amount")
        amt_str = _coerce_amount_str(amt_val)
        if amt_str is not None:
            lines.append(f"T{amt_str}")

        # Payee / Description
        payee = rec.get("payee") or rec.get("description")
        if payee:
            clean_payee = str(payee).strip().replace("\n", " ")
            if clean_payee:
                lines.append(f"P{clean_payee}")

        # Memo
        memo = rec.get("memo") or rec.get("extra_info")
        if memo:
            clean_memo = str(memo).strip().replace("\n", " ")
            if clean_memo:
                lines.append(f"M{clean_memo}")

        # Reference / Check number
        ref = rec.get("reference") or rec.get("check_number")
        if ref:
            clean_ref = str(ref).strip()
            if clean_ref:
                lines.append(f"N{clean_ref}")

        # Category
        cat = rec.get("category")
        if cat:
            clean_cat = str(cat).strip()
            if clean_cat:
                lines.append(f"L{clean_cat}")

        # End of record
        lines.append("^")

    return "\n".join(lines) + "\n"


def write_qif(
    data: (
        Sequence[Transaction]
        | pd.DataFrame
        | Sequence[Mapping[str, Any]]
        | Any
    ),
    destination: str | os.PathLike[str],
    account_type: str = "Bank",
    date_format: str = "%Y-%m-%d",
) -> Path:
    """Write transactions to a QIF file on disk.

    Args:
        data: Transactions as DataFrame, Transaction list, or dict records.
        destination: Path to write the output QIF file.
        account_type: QIF header type (default 'Bank').
        date_format: Date format string for 'D' fields.

    Returns:
        Path object pointing to the written file.
    """
    content = to_qif(data, account_type=account_type, date_format=date_format)
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target
