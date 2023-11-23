import sys
import os

sys.path.append(__file__.removesuffix("/benchmark/util/count_joins.py"))
from benchmark.tools.query_parser import get_joins, load_query

# Given a directory, this code parses every sql query in the directory and prints out the number of joins in that query.
if __name__ == "__main__":
    queries_dir = sys.argv[1]

    # Use os.scandir to get an iterator of os.DirEntry objects
    # in the specified directory
    queries = os.scandir(queries_dir)
    sorted_queries = sorted(queries, key=lambda entry: entry.name)

    # Print all files and directories in the specified path
    print(f"Files and Directories in {queries_dir}:")
    lengths = []
    for query in sorted_queries:
        try:
            lines = open(query.path, "r").readlines()
            query_str = " ".join([line.strip() for line in lines])
            lengths.append(f"{query.name}: {len(get_joins(query_str))}")
        except:
            print(f"{query.name}: failed")
    print(*lengths, sep="\n")
