import json
import sys

from benchmark.run.individual import main_approx_time_mem, main_comp_card_est, main_parse, main_time_mem, main_run
from benchmark.engine.engine import set_engine
from benchmark.tools.schema import get_schema

# This program accepts a number of positional arguments, and optional arguments.
#   1st arg: running configuration, can be one of the following:
#       - schema: parses the db schema
#       - parse: parses the db query
#       - run: executes a query
#       - time_mem: executes a query and logs some time and memory usage information
#       - approx_time_mem: performs cost model approximation for a query
#       - optim_nsga_ii: performs join order optimization for a query
#       - comp_card_est: runs a query, and calculates the cardinality estimate for the cost model, then compares the two
#   2nd arg: db_set/query in that format, for some run configurations the query might be omitted
#   opt arg: --db-path [path/to/database] a custom path to the database, otherwise defaults to ./data/{{db_set}} the directory must include the following files:
#       - schema.sql: the schema of the dataset
#       - queries/*.sql: queries for the dataset
#       - tables/*.(csv|tbl): tables for the dataset
# Additionally each configuration might specify additional required or optional parameters.
if __name__ == "__main__":
    print(f'Running with args: {sys.argv}')
    
    run_config = sys.argv[1]
    [db_set, query] = sys.argv[2].split("/")
    
    if '--gpu' in sys.argv:
        set_engine('gpu')
    else: # default to cpu
        set_engine('cpu')
        
    manual_parse = False
    if '--manual-parse' in sys.argv:
        manual_parse = True
    
    db_path = f'./data/{db_set}'
    if '--db-path' in sys.argv:
        dbp_arg = sys.argv.index('--db-path')
        if len(sys.argv) <= dbp_arg + 1:
            print('Error: Not enough arguments after --db-path statement, must follow the format: "--db-path [path/to/database]"')
            exit(1)
        db_path = sys.argv[ + 1]
        
    
    # Loads the schema, usually used for testing
    #     2nd arg: db_set (if provided with '/query' suffix, it's ignored)
    if run_config == 'schema':
        db_set = sys.argv[2]
        schema = json.dumps(get_schema(db_path, db_set), indent="\t")
        print(f"Parsed schema:\n{schema}")
        
    # Parses the query, usually used for testing
    elif run_config == 'parse':
        main_parse.main(db_path, db_set, query, manual_parse)
        
    # run - just execute the query with given join order (for use when timed outside)
    #     3rd arg: order of joins
    #     opt arg --skip-joins: skips all joins
    #     opt arg --log [filename] [start of log]: opens the log file and prints the start of the log and measures times of each operation such as filters and joins
    elif run_config == 'run':
        if query == None:
            query = db_set
            db_set = "ssb" # Default to ssb
        perm = [int(i) for i in sys.argv[3].split(',')]
        skip_joins = True if '--skip-joins' in sys.argv else False
        
        if '--log' in sys.argv:
            log_arg = sys.argv.index('--log')
            if len(sys.argv) <= log_arg + 2:
                print('Error: Not enough arguments after --log statement, must follow the format: "--log [filename] [log_start]"')
                exit(1)
            log_file = sys.argv[log_arg + 1]
            log_head = sys.argv[log_arg + 2]
            main_run.main(db_path, db_set, query, perm, skip_joins, manual_parse, log_file, log_head)
            
        # No logging inside python
        else:
            main_run.main(db_path, db_set, query, perm, skip_joins, manual_parse)
        
        
    # time_mem_log - measure the time and peak memory use
    #     3rd arg: order of joins    
    elif run_config == 'time_mem':
        if query == None:
            query = db_set
            db_set = "ssb" # Default to ssb
        perm = [int(i) for i in sys.argv[3].split(',')]
        main_time_mem.main(db_path, db_set, query, perm)
    
    # approx_time_mem - use the cost model to calculate the time and memory cost
    #     3rd arg: order of joins
    elif run_config == 'approx_time_mem':
        if query == None:
            print("No query specified")
            exit(1)
        perm = [int(i) for i in sys.argv[3].split(',')]
        main_approx_time_mem.main(db_path, db_set, query, perm)
    
    # optim_nsga_ii - use the nsga_ii optimization algorithm and the time_mem cost model to find the pareto front
    elif run_config == 'optim_nsga_ii':
        if query == None:
            print("No query specified")
            exit(1)
            
        # IMPORT IS HERE, TO AVOID HAVING TO IMPORT THE OPTIMIZATION FRAMEWORK IF WE ARE NOT USING IT
        from benchmark.run.optimization import main_optim_nsga_ii
        main_optim_nsga_ii.main(db_path, db_set, query)
        
        
    # comp_card_est - combination of 'run' and 'approximation' but focus on the accuracy of cardinality estimate
    #     3rd arg: order of joins
    elif run_config == 'comp_card_est':
        if query == None:
            print("No query specified")
            exit(1)
        perm = [int(i) for i in sys.argv[3].split(',')]
        main_comp_card_est.main(db_path, db_set, query, perm)
        
    else:
        print("Selected RUN configuration not specified.")
