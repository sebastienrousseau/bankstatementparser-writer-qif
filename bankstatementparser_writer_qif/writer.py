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


def _parse_amount_text(text: str) -> tuple[Decimal | None, str]:
    """Parse amount text (commas dropped) and return it with the text."""
    as_given = text.strip().replace(",", "")
    try:
        return Decimal(as_given), as_given
    except Exception:
        return None, as_given


def _coerce_amount_str(val: Any) -> str | None:
    """Coerce amount values to decimal string with 2 decimal places.

    Text that does not parse is written as given. So is an amount of
    1E+26 or more, which needs more than 28 significant digits at cent
    precision: "1E+999999999" would otherwise expand to a billion
    digits. ``adjusted()`` keeps that check cheap, as this runs once per
    record.
    """
    if val is None:
        return None
    if isinstance(val, float):
        return None if pd.isna(val) else f"{val:.2f}"
    if isinstance(val, str):
        amount, as_given = _parse_amount_text(val)
        if amount is None:
            return as_given or None
    elif isinstance(val, (Decimal, int)):
        amount, as_given = Decimal(val), str(val)
    else:
        return str(val)
    if amount.is_finite() and amount.adjusted() >= 26:
        return as_given
    return f"{amount:.2f}"


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


def _record_lines(rec: Mapping[str, Any], date_format: str) -> list[str]:
    """The ``D``/``T``/``P``/``M``/``N``/``L`` lines and ``^`` for a record.

    QIF is one field per line, so every line break inside a value
    (whatever ``str.splitlines`` splits on) becomes a space: otherwise
    it would start a field, or with ``^`` a record, of its own. The
    normalisation is inline rather than a helper because this runs once
    per field of every record.
    """
    raw_date = (
        rec.get("date") or rec.get("booking_date") or rec.get("value_date")
    )
    fields = (
        ("D", _coerce_date_str(raw_date, date_format)),
        ("T", _coerce_amount_str(rec.get("amount"))),
        ("P", rec.get("payee") or rec.get("description")),
        ("M", rec.get("memo") or rec.get("extra_info")),
        ("N", rec.get("reference") or rec.get("check_number")),
        ("L", rec.get("category")),
    )
    lines = []
    for code, value in fields:
        text = " ".join(str(value).splitlines()).strip() if value else ""
        if text:
            lines.append(code + text)
    lines.append("^")
    return lines


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
        lines.extend(_record_lines(rec, date_format))
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
