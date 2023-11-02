import sys

from benchmark.run.individual import main_approx_time_mem, main_comp_card_est, main_parse, main_time_mem, main_run
# from benchmark.run.optimization import main_optim_nsga_ii
from benchmark.engine.engine import set_engine
from benchmark.tools.schema import get_schema

# This program accepts a number of positional arguments. 
# The first argument is the name of the program to run, it can be one of the following:
if __name__ == "__main__":
    print(f'Running with args: {sys.argv}')    
    
    if '--gpu' in [a.lower() for a in sys.argv]:
        set_engine('gpu')
    else: # default to cpu
        set_engine('cpu')
        
    manual_parse = False
    if '--manual-parse' in [a.lower() for a in sys.argv]:
        manual_parse = True
        
    run_config = sys.argv[1]
    
    # Loads the schema, usually used for testing
    #     2nd arg: db_name
    if run_config == 'schema' :
        db_set = sys.argv[2]
        get_schema(db_set)
        
    # Parses the query, usually used for testing
    #     2nd arg: db_set/query 
    if run_config == 'parse':
        [db_set, query] = sys.argv[2].split("/")
        main_parse.main(db_set, query, manual_parse)
        
    # run - just execute the query with given join order (for use when timed outside)
    #     2nd arg: db_set/query 
    #     3rd arg: order of joins    
    if run_config == 'run':
        [db_set, query] = sys.argv[2].split("/")
        if query == None:
            query = db_set
            db_set = "ssb" # Default to ssb
        perm = [int(i) for i in sys.argv[3].split(',')]
        skip_joins = True if '--skip-joins' in [a.lower() for a in sys.argv] else False
        main_run.main(db_set, query, perm, skip_joins, manual_parse)
    
    # time_mem_log - measure the time and peak memory use
    #     2nd arg: db_set/query 
    #     3rd arg: order of joins    
    if run_config == 'time_mem':
        [db_set, query] = sys.argv[2].split("/")
        if query == None:
            query = db_set
            db_set = "ssb" # Default to ssb
        perm = [int(i) for i in sys.argv[3].split(',')]
        main_time_mem.main(db_set, query, perm)
    
    # approx_time_mem - use the cost model to calculate the time and memory cost
    #     2nd arg: db_set/query 
    #     3rd arg: order of joins
    if run_config == 'approx_time_mem':
        [db_set, query] = sys.argv[2].split("/")
        if query == None:
            print("No query specified")
            exit(1)
        perm = [int(i) for i in sys.argv[3].split(',')]
        main_approx_time_mem.main(db_set, query, perm)
    
    # # optim_nsga_ii - use the nsga_ii optimization algorithm and the time_mem cost model to find the pareto front
    # #     2nd arg: db_set/query
    # if run_config == 'optim_nsga_ii':
    #     [db_set, query] = sys.argv[2].split("/")
    #     if query == None:
    #         print("No query specified")
    #         exit(1)
    #     main_optim_nsga_ii.main(db_set, query)
        
        
    # comp_card_est - combination of 'run' and 'approximation' but focus on the accuracy of cardinality estimate
    #     2nd arg: db_set/query 
    #     3rd arg: order of joins
    if run_config == 'comp_card_est':
        [db_set, query] = sys.argv[2].split("/")
        if query == None:
            print("No query specified")
            exit(1)
        perm = [int(i) for i in sys.argv[3].split(',')]
        main_comp_card_est.main(db_set, query, perm)
