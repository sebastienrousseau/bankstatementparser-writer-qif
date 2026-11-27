# Benchmarks

`benches/bench_to_qif.py` measures one `to_qif` call as the statement
grows, for each input shape the writer accepts: a list of `Transaction`
objects, a pandas DataFrame and a list of dicts. Each figure is the best
of five runs after one warm-up. Nothing asserts a threshold: wall-clock
is not comparable between machines. CI runs
`python benches/bench_to_qif.py --quick` on every operating system and
Python in the test matrix so the benchmark keeps running against the
current API.

## Results

Run with `poetry run python benches/bench_to_qif.py` on 2026-11-27:
Apple M1 Pro, macOS 27.2.1, CPython 3.12.16,
bankstatementparser-writer-qif 0.0.36 with bankstatementparser 0.0.35.

| Transactions | QIF KiB | Transactions ms | DataFrame ms | Dicts ms |
| ---: | ---: | ---: | ---: | ---: |
| 10 | 0.5 | 0.03 | 0.19 | 0.03 |
| 100 | 5.0 | 0.31 | 1.61 | 0.30 |
| 1,000 | 51.2 | 3.07 | 16.71 | 3.03 |
| 10,000 | 521.4 | 33.40 | 165.78 | 30.98 |

Cost is linear in every shape: the per-transaction figure at 10,000
records is within 15% of the figure at 10 (about 3 us for dicts and
`Transaction` objects, 17 us for a DataFrame, whose rows are converted
to dicts first).

Reproduce with `python benches/bench_to_qif.py` (add `--json` for
machine-readable output).
