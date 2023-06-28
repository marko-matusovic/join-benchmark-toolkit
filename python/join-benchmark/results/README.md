# Results Folder

This folder stores all results from the runs. Over time the measurements change, but the old results stay in this folder.

The various running setup is explained here for each folder:

- [**bad_measurement_setup**](bad_measurement_setup)
  - Results from measurements that perform all runs with loaded data in memory.
- [**time_mem**](time_mem)
  - Each run is individual.
  - Measurements are performed within the python program.
  - This gives detailed information about how much memory and time cost each join operation.
- [**ncu**](ncu) (⭐️)
  - Results from Profiling with the ncu toolkit.
  - Interesting data from this are the memory usage per kernel.
  - Each permutation (its own run) is stored individually in a file.
- [**external_log**](external_log) (⭐️)
  - Timing results from a basic run on CPU or GPU.
  - Measurements are performed externally.
- [**approx_time_mem**](approx_time_mem)
  - Results from the cost model.
- [**optimization**](optimization)
  - Results from the optimization.
