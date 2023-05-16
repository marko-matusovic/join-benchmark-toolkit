
import sys

from benchmark.run.individual import main_time_mem
from benchmark.run.individual import main_run

# This program accepts a number of positional arguments. 
# The first argument is the name of the program to run, it can be one of the following:
# 
# run - just execute the query with given join order (for use when timed outside)
#     2nd arg: db_set/query 
#     3rd arg: order of joins
# time_mem_log - measure the time and peak memory use
#     2nd arg: db_set/query 
#     3rd arg: order of joins
if __name__ == "__main__":
    run_config = sys.argv[1]
    if run_config == 'run':
        [db_set, query] = sys.argv[2].split("/")
        if query == None:
            query = db_set
            db_set = "ssb" # Default to ssb
        perm = [int(i) for i in sys.argv[3].split(',')]
        main_run.main(db_set, query, perm)
    if run_config == 'time_mem':
        [db_set, query] = sys.argv[2].split("/")
        if query == None:
            query = db_set
            db_set = "ssb" # Default to ssb
        perm = [int(i) for i in sys.argv[3].split(',')]
        main_time_mem.main(db_set, query, perm)