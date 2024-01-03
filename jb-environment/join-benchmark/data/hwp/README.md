# Hardware Probing Database

The purpose of this dataset is to generate a set of dummy scenarios that test various hardware features of the system running the **Join Benchmark Framework**.

The directory `/scripts` contains scripts that generate files in the `/tables` directory. You can trigger this by running the `/scripts/tbl_gen.sh` script.

## Table Structure

Each table has the following columns: `| id | value | some_key |`.

| Field      | Data Type |
| ---------- | --------- |
| `id`       | int       |
| `value`    | char(64)  |
| `some_key` | int       |

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

- **small**: 1 000 rows
- **medium**: 100 000 rows
- **large**: 10 000 000 rows

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
