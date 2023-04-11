
import sys

from benchmark.run import main_time_mem


if __name__ == "__main__":
    run_config = sys.argv[1]
    if run_config == 'time_mem':
        main_time_mem.main(sys.argv[2:])