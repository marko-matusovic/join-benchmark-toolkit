# Join Benchmark Toolkit

This repository is a home to the join benchmark toolkit, as well as three database generation tools.

```
├── imdb-db-tool
├── ssb-dbgen
├── tpcds-kit
└── jb-environment
    └── join-benchmark
```

## Join Benchmark Toolkit
is a modular SQL engine with parsing, optimization, and execution support. It can execute operations on CPU or GPU, and a new DB set can be easily connected.

Located in [./jb-environment/join-benchmark](./jb-environment/join-benchmark)

## JBT Environment
defines the environment for _Join Benchmark Toolkit_ with scripts for simple startup.
    
Located in [./jb-environment](./jbt-environment)

## DB Generators
- **JOB**: [imdb-db-tool](./imdb-db-tool) contains tools for fetching and setting up the imdb dataset for _join order benchmark_.
- **SSB**: [ssb-dbgen](./ssb-dbgen) contains tools for generating queries and tables for _Star Schema Benchmark_.
- **TPC-DS**: [tpcds-kit](./tpcds-kit) contains tools for generating queries and tables for _Star Schema Benchmark_.
