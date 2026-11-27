# bankstatementparser-writer-qif

**QIF** (Quicken Interchange Format) is a line-based text format that
accounting and personal-finance tools such as GnuCash, Moneydance,
Quicken and YNAB import. **bankstatementparser-writer-qif** writes
transactions parsed by
[`bankstatementparser`](https://github.com/sebastienrousseau/bankstatementparser)
as a QIF file: a `!Type:` header, then one record per transaction ending
in `^`.

| Concern | How this writer handles it |
| :--- | :--- |
| Input | `list[Transaction]`, a `pandas.DataFrame`, `list[dict]`, or a core parser object |
| Account type | The `!Type:` header, `Bank` by default (`CCard`, `Cash` and others as given) |
| Fields | `D` (date), `T` (amount), `P` (payee), `M` (memo), `N` (reference or check number), `L` (category), `^` (end) |
| Dates | ISO `YYYY-MM-DD` by default; any `strftime` format, such as Quicken's `%m/%d/%Y` |
| Safety | Every line break in a value becomes a space, so text cannot start a field or record |

```python
from bankstatementparser import create_parser

from bankstatementparser_writer_qif import write_qif

parser = create_parser("statement.csv")
write_qif(parser, "statement.qif", date_format="%m/%d/%Y")
```

## In this manual

- [Usage](usage.md): inputs, field mapping, options and limits.
- [Architecture](architecture.md): how the module is laid out.
- [The suite](suite.md): the `bankstatementparser` packages.
- [Comparison](COMPARISON.md) and [Benchmarks](BENCHMARKS.md).
- [Supported Python policy](POLICIES.md).
- [API reference](api.md), generated from the docstrings.
- [Changelog](changelog.md) and [Security policy](security.md).

The source, issues and releases live on
[GitHub](https://github.com/sebastienrousseau/bankstatementparser-writer-qif);
the package is on
[PyPI](https://pypi.org/project/bankstatementparser-writer-qif/).
