
import sys

from benchmark.run.individual import main_time_mem
from benchmark.run.individual import main_run
from benchmark.engine.engine import set_engine

from benchmark.run.all_together import main_approx_time
from benchmark.run.individual import main_approx_gpu_time_mem

# This program accepts a number of positional arguments. 
# The first argument is the name of the program to run, it can be one of the following:
if __name__ == "__main__":
    if '--gpu' in [a.lower() for a in sys.argv]:
        set_engine('cudf')
    else:
        set_engine('pandas')
        
    # run - just execute the query with given join order (for use when timed outside)
    #   2nd arg: db_set/query
    #   3rd arg: order of joins
    run_config = sys.argv[1]
    if run_config == 'run':
        [db_set, query] = sys.argv[2].split("/")
        if query == None:
            query = db_set
            db_set = "ssb" # Default to ssb
        perm = [int(i) for i in sys.argv[3].split(',')]
        main_run.main(db_set, query, perm)
        
        
    # time_mem_log - measure the time and peak memory use
    #   2nd arg: db_set/query 
    #   3rd arg: order of joins        
    elif run_config == 'time_mem':
        [db_set, query] = sys.argv[2].split("/")
        if query == None:
            query = db_set
            db_set = "ssb" # Default to ssb
        perm = [int(i) for i in sys.argv[3].split(',')]
        main_time_mem.main(db_set, query, perm)
        
        
    # approx_time - initial attempt at time cost model
    #   2nd arg: ssb/query or query (this approx config only works for ssb)
    elif run_config == 'approx_time':
        [db_set, query] = sys.argv[2].split("/")
        
        if query == None:
            query = db_set
            db_set = "ssb" # Default
        
        if db_set != "ssb":
            print("Time approximation is only configured for SSB")
            exit(1)

        main_approx_time.main(db_set, query)
    
    
    # approx_gpu_time_mem - new approach to cost models for both time and memory for GPU
    #   2nd arg: 'db_set/query' or 'query' where we default to db_set='job'
    #   3rd arg: order of joins
    elif run_config == "approx_gpu_time_mem":
        [db_set, query] = sys.argv[2].split("/")
        
        if query == None:
            query = db_set
            db_set = "job" # Default
        
        perm = [int(i) for i in sys.argv[3].split(',')]
        main_approx_gpu_time_mem.main(query, db_set, perm)