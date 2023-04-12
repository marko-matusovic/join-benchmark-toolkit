
import sys

from benchmark.run import main_time_mem


if __name__ == "__main__":
    run_config = sys.argv[1]
    if run_config == 'time_mem':
        [db_set, query] = sys.argv[2].split("/")
        if query == None:
            query = db_set
            db_set = "ssb"
        perm = [int(i) for i in sys.argv[3].split(',')]
        main_time_mem.main(db_set, query, perm)