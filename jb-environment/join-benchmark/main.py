import json
import os
import sys

from benchmark.run.individual import (
    main_approx_time_mem,
    main_comp_card_est,
    main_parse,
    main_run_time_mem,
    main_run,
    main_features,
)
from benchmark.run.train import main_train_gbdt_aet, main_evaluate_gbdt_aet, main_train_gbdt_cmp, main_evaluate_gbdt_cmp
from benchmark.engine.engine import set_engine
from benchmark.tools.schema_parser import get_schema


# Returns a list of values following a named argument
def named_arg(arg: str, count: int) -> list[str]:
    if arg not in sys.argv:
        return []

    arg_idx = sys.argv.index(arg)
    if len(sys.argv) < arg_idx + 1 + count:
        print(f"ERROR: named argument {arg} must follow with at least {count} values!")
        exit(1)

    return sys.argv[arg_idx + 1 : arg_idx + 1 + count]


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
#   3rd arg (sometimes): join order, in format "0,1,2,3"
#   opt arg: --db-path [path/to/database] a custom path to the database, otherwise defaults to ./data/{{db_set}} the directory must include the following files:
#       - schema.sql: the schema of the dataset
#       - queries/*.sql: queries for the dataset
#       - tables/*.(csv|tbl): tables for the dataset
# Additionally each configuration might specify additional required or optional parameters.
if __name__ == "__main__":
    print(f"Running with args: {sys.argv}")

    run_config = sys.argv[1]
    (db_set, _sep, query) = sys.argv[2].partition("/")

    if "--gpu" in sys.argv:
        set_engine("gpu")
    else:  # default to cpu
        set_engine("cpu")

    manual_parse = False
    if "--manual-parse" in sys.argv:
        manual_parse = True

    if "--db-path" in sys.argv:
        db_path = named_arg("--db-path", 1)[0]
    else:
        this_path = os.path.abspath(__file__).removesuffix("/main.py")
        db_path = f"{this_path}/data/{db_set}"

    # Loads the schema, usually used for testing
    #     2nd arg: db_set (if provided with '/query' suffix, it's ignored)
    if run_config == "schema":
        schema = json.dumps(get_schema(db_path, db_set), indent="\t")
        print(f"Parsed schema:\n{schema}")

    # Parses the query, usually used for testing
    elif run_config == "parse":
        main_parse.main(db_path, db_set, query, manual_parse)

    # run - just execute the query with given join order (for use when timed outside)
    #     opt arg --jo [integer sequence] order of joins
    #     opt arg --skip-joins: skips all joins
    #     opt arg --log-time [filename] [start of log]: opens the log file and prints the start of the log and measures times of each operation such as filters and joins
    #     opt arg --log-time-mem [filename] [start of log]: opens the log file and prints the start of the log and measures times of each operation such as filters and joins
    elif run_config == "run":
        perm = (
            [int(i) for i in named_arg("--jo", 1)[0].split(",")]
            if "--jo" in sys.argv
            else None
        )

        skip_joins = True if "--skip-joins" in sys.argv else False

        if "--log-time" in sys.argv and "--log-time-mem" in sys.argv:
            print(
                "ERROR: Cannot run with both --log-time and --log-time-mem parameters, choose one!"
            )
            exit(1)

        if "--log-time" in sys.argv:
            [log_file, log_head] = named_arg("--log-time", 2)
            main_run.main(
                db_path,
                db_set,
                query,
                perm,
                skip_joins,
                manual_parse,
                log_file,
                log_head,
                "--save" in sys.argv,
            )

        elif "--log-time-mem" in sys.argv:
            [log_file, log_head] = named_arg("--log-time-mem", 2)
            main_run_time_mem.main(
                db_path,
                db_set,
                query,
                perm,
                skip_joins,
                manual_parse,
                log_file,
                log_head,
            )

        # No logging inside python
        else:
            main_run.main(
                db_path,
                db_set,
                query,
                perm,
                skip_joins,
                manual_parse,
                save_res="--save" in sys.argv,
            )

    # Generates a list of features for training
    elif run_config == "features":
        perm = (
            [int(i) for i in named_arg("--jo", 1)[0].split(",")]
            if "--jo" in sys.argv
            else None
        )

        log_file = None
        log_head = ""
        if "--log" in sys.argv:
            [log_file, log_head] = named_arg("--log", 2)

        main_features.main(
            db_path,
            db_set,
            query,
            perm,
            log_file,
            log_head,
            manual_parse,
        )

    # approx_time_mem - use the cost model to calculate the time and memory cost
    #     opt arg --jo [integer sequence]: order of joins
    elif run_config == "approx_time_mem":
        if query == None:
            print("No query specified")
            exit(1)
        perm = (
            [int(i) for i in named_arg("--jo", 1)[0].split(",")]
            if "--jo" in sys.argv
            else None
        )
        main_approx_time_mem.main(db_path, db_set, query, perm)

    # optim_nsga_ii - use the nsga_ii optimization algorithm and the time_mem cost model to find the pareto front
    elif run_config == "optim_nsga_ii":
        if query == None:
            print("No query specified")
            exit(1)

        # IMPORT IS HERE, TO AVOID HAVING TO IMPORT THE OPTIMIZATION FRAMEWORK IF WE ARE NOT USING IT
        from benchmark.run.optimization import main_optim_nsga_ii

        main_optim_nsga_ii.main(db_path, db_set, query)

    # comp_card_est - combination of 'run' and 'approximation' but focus on the accuracy of cardinality estimate
    elif run_config == "comp_card_est":
        if query == None:
            print("No query specified")
            exit(1)
        perm = (
            [int(i) for i in named_arg("--jo", 1)[0].split(",")]
            if "--jo" in sys.argv
            else None
        )
        main_comp_card_est.main(db_path, db_set, query, perm)

    # start training a model
    #   2rd arg: a comma separated list of db_set names to train on.
    #   3rd arg: id of the training set [integer]
    #   4th arg: name of the hardware for hw features
    #   opt arg: --joins-in-block {{int}} the number of joins in a single block
    #   opt arg: --res-path {{str}} path to the res dir
    elif run_config == "train-aet":
        db_sets = [db_set.strip() for db_set in sys.argv[2].split(",")]
        training_set = int(sys.argv[3])
        hw_name = sys.argv[4]
        res_path = (
            None if "--res-path" not in sys.argv else named_arg("--res-path", 1)[0]
        )
        joins_in_block = (
            4
            if "--joins-in-block" not in sys.argv
            else int(named_arg("--joins-in-block", 1)[0])
        )
        main_train_gbdt_aet.main(
            db_sets, training_set, hw_name, joins_in_block, res_path
        )

    # Evaluate a trained ML model
    #   2rd arg: name of the db_set to be evaluated
    #   3rd arg: id of the training set [integer]
    #   4th arg: name of the hardware for hw features
    #   5th arg: name of the ML model
    #   opt arg: --res-path {{str}} path to the res dir
    elif run_config == "eval-aet":
        db_sets = sys.argv[2]
        training_set = int(sys.argv[3])
        hw_name = sys.argv[4]
        model_name = sys.argv[5]
        res_path = (
            None if "--res-path" not in sys.argv else named_arg("--res-path", 1)[0]
        )
        main_evaluate_gbdt_aet.main(db_set, training_set, model_name, hw_name, res_path)
    
    # start training a model
    #   2rd arg: a comma separated list of db_set names to train on.
    #   3rd arg: id of the training set [integer]
    #   4th arg: name of the hardware for hw features
    #   req arg: --num-joins {{int}} the number of joins
    #   opt arg: --res-path {{str}} path to the res dir
    elif run_config == "train-cmp":
        db_sets = [db_set.strip() for db_set in sys.argv[2].split(",")]
        training_set = int(sys.argv[3])
        hw_name = sys.argv[4]
        res_path = (
            None if "--res-path" not in sys.argv else named_arg("--res-path", 1)[0]
        )
        if "--num-joins" not in sys.argv:
            print("Please specify the number of joins with --num-joins {{int}}")
        num_joins = int(named_arg("--num-joins", 1)[0])
        main_train_gbdt_cmp.main(
            db_sets, training_set, hw_name, num_joins, res_path
        )

    # Evaluate a trained ML model
    #   2rd arg: name of the db_set to be evaluated
    #   3rd arg: id of the training set [integer]
    #   4th arg: name of the hardware for hw features
    #   5th arg: name of the ML model
    #   opt arg: --res-path {{str}} path to the res dir
    elif run_config == "eval-cmp":
        db_sets = sys.argv[2]
        training_set = int(sys.argv[3])
        hw_name = sys.argv[4]
        model_name = sys.argv[5]
        res_path = (
            None if "--res-path" not in sys.argv else named_arg("--res-path", 1)[0]
        )
        main_evaluate_gbdt_cmp.main(db_set, training_set, model_name, hw_name, res_path)

    else:
        print("Selected RUN configuration not specified.")
