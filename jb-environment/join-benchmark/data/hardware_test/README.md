# Hardware Test Database

The purpose of this dataset is to generate a set of dummy scenarios that test various hardware features of the system running the **Join Benchmark Framework**.

The directory `/scripts` contains scripts that generate files in the `/tables` directory. You can trigger this by running the `/scripts/tbl_gen.sh` script.

## Table Structure

Each table has the following columns: `| id | value | some_key |`.

| Field      | Size [Bytes] |
| ---------- | ------------ |
| `id`       | 32           |
| `value`    | 256          |
| `some_key` | 32           |

> We encode the table in UTF-8, with [a-zA-Z0-9] characters, thus each character is 8 bits = 1byte, so the number of bytes is the same as the number of characters

Fields `id` and `value` are unique, `some_key` can have duplicates and is sometimes used to reference some other table.

## Test Scenarios

This section describes the different test scenarios that are generated:

- **copy table to GPU**
  - selects all values from *one* table
- **1-to-1 join**
  - every value in table A is unique, and matches 1-to-1 with table B
- **1-to-n join**
  - each value in table A is unique, values of table B is a subset of values of table A, each value in A can match [0,n] rows in table B
- **n-to-n join**
  - Both tables A and B contain values not in their intersection, and both values in A and B can match [0,n] rows in the other table

In addition, we test each scenario at a scale:

- **small**: 100 rows
- **medium**: 10 000 rows
- **large**: 1 000 000 rows

Each query (in `/queries` directory) uses one scenario and one scale. The query name follows the following format: `query_{scenario}_{scale}.sql`

Where scenario is one of the following:

- `cp`: **copy table to GPU**
- `11`: **1-to-1 join**
- `1n`: **1-to-n join**
- `nn`: **n-to-n join**

and scale one of the following:

- `sm`: **small**
- `md`: **medium**
- `lg`: **large**
