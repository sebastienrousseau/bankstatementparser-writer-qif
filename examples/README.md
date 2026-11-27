# Examples for bankstatementparser-writer-qif

Runnable scripts, each run in CI (`for f in examples/*.py`) and by
`tests/test_regression_examples.py`.

- `01_basic_usage.py`: serialises two `Transaction` objects with
  `to_qif`, with ISO dates and then with `MM/DD/YYYY` dates and a
  `CCard` account type.
- `02_advanced_workflow.py`: parses [`data/statement.csv`](data/statement.csv)
  with the core `bankstatementparser`, writes it with `write_qif` to a
  temporary directory and summarises the file.
