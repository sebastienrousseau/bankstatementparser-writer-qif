# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Concurrency and stress tests for QIF writer."""

import time
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

import pytest
from bankstatementparser.transaction_models import Transaction

from bankstatementparser_writer_qif import to_qif


# A throughput threshold measures the writer, not coverage's tracer:
# without sys.monitoring (CPython 3.10 and 3.11) tracing every line of
# eight threads made the same work several times slower on CI runners.
@pytest.mark.no_cover
def test_qif_writer_concurrency() -> None:
    """Verify QIF export throughput under concurrent execution."""
    txns = [
        Transaction(
            account_id="ACC1",
            amount=Decimal("123.45"),
            currency="USD",
            description="Office Supplies",
            reference="REF001",
        )
        for _ in range(100)
    ]

    iterations = 500
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(to_qif, txns) for _ in range(iterations)]
        results = [f.result() for f in futures]
    elapsed = time.perf_counter() - start

    assert len(results) == iterations
    for qif_str in results:
        assert "!Type:Bank" in qif_str
        assert "T123.45" in qif_str
    assert elapsed < 5.0
