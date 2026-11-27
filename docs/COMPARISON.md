# Comparison

Where bankstatementparser-writer-qif fits next to what a reader would
otherwise reach for. Every cell comes from this repository or the other
project's own PyPI description; nothing here is a measured ranking.

| Project | Writes QIF | Reads QIF | Investments, splits, categories as objects | Input it writes from |
| :--- | :---: | :---: | :---: | :--- |
| **bankstatementparser-writer-qif** | Yes | No | No (a category is an `L` line) | `bankstatementparser` transactions, DataFrames, dicts |
| [`quiffen`](https://pypi.org/project/quiffen/) (MIT) | Yes | Yes | Yes | Its own QIF object model |

## When each fits

- **bankstatementparser-writer-qif**: your statements are already
  parsed by `bankstatementparser` (CAMT, MT940, CSV and the rest) and
  you want a bank-type QIF file in one call.
- **quiffen**: you need to read QIF, or to write investments, splits,
  several accounts or category lists.

The wider family is listed in [The suite](suite.md).
