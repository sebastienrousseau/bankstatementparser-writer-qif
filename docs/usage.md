# Usage

## Inputs

`to_qif(data, ...)` and `write_qif(data, destination, ...)` accept:

- a list of `bankstatementparser` `Transaction` objects;
- a pandas DataFrame, each row a record;
- a list of mappings (dicts);
- any object with a `to_transactions()` method, or a `parse()` method
  returning a DataFrame (the core parsers), which is called first.

Items in a list that are neither a `Transaction` nor a mapping are
skipped.

## Field mapping

Each record is written as the lines below, in this order, then `^`. A
line is left out when its value is missing or empty.

| QIF line | Taken from |
| :--- | :--- |
| `D` | `date`, else `booking_date`, else `value_date` (a `Transaction` gives its booking date, else its value date), formatted with `date_format`; an ISO string is reformatted, any other string is written as it is |
| `T` | `amount` with two decimals; a string that does not parse, or an amount of 1E+26 or more (beyond 28 significant digits at cent precision), is written as given |
| `P` | `payee`, else `description` |
| `M` | `memo`, else `extra_info` (a `Transaction` gives its reference, else its transaction ID) |
| `N` | `reference`, else `check_number` |
| `L` | `category` |

Every value is trimmed and every line break in it becomes a space.

## Options

| Argument | Default | Meaning |
| :--- | :--- | :--- |
| `account_type` | `"Bank"` | The header, written as `!Type:<account_type>` (`Bank`, `CCard`, `Cash` and so on) |
| `date_format` | `"%Y-%m-%d"` | The `strftime` format for `D` lines, e.g. `"%m/%d/%Y"` for Quicken |

`write_qif` writes UTF-8 text to `destination`, creating missing parent
directories, and returns the `Path`.

## Limits

- One account per file, and no `!Account` block.
- Bank-style records only: no investment (`!Type:Invst`) fields, splits
  or memorised transactions.
- No currency: QIF has no currency field, so amounts are written as
  numbers only.
- QIF has no escape syntax; apart from line breaks, values are written
  as they are.
