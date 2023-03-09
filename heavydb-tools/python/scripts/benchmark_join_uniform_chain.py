from heavyai import connect
from pandas import DataFrame
import sys
import numpy as np
from numpy.random import default_rng
from time import time

TABLES = ['P', 'R', 'S', 'T', 'U']

def main(join_count, repeat):
    db = connect(user="admin", password="HyperInteractive", host="mm_heavydb", dbname="heavyai")

    print('Running benchmark on uniform join.')
    print(f'For {join_count} tables: {", ".join(TABLES[:join_count])}')
    print(f'Repeating {repeat} times.')

    query = build_query(join_count)

    print(f'With query:\n{query}')

    # for count in ['1k', '10k', '100k', '1m', '10m']:
    for count in ['100m']:
        times = []
        start = time()
        print(f'Times for {count}:', end=' ')
        for i in range(repeat):
            clear_tables(db)
            fill_tables(db, join_count, parse_int(count))

            time_a = time()
            res = db.select_ipc(query)
            time_b = time()

            times.append(time_b - time_a)
            print(f'{times[-1]}', end=', ')
        print()
        print(f'Average time: {np.average(times)}')
        print(f'Benchmark time: {time() - start}')

def parse_int(str_int):
    exp = {
        'k': 1e3,
        'm': 1e6,
        'g': 1e9
    }
    if str_int[-1].lower() in exp:
        return int(int(str_int[:-1]) * exp[str_int[-1].lower()])
    else:
        return int(str_int)

def build_query(join_count):
    q_select = ', '.join([ f'table_{t}.key AS key_{t}, table_{t}.val AS val_{t}' for t in TABLES[:join_count] ])
    q_from = ', '.join([ f'table_{t}' for t in TABLES[:join_count] ])
    q_where = ' AND '.join([ f'table_{TABLES[ti]}.val=table_{TABLES[ti+1]}.key' for ti in range(join_count-1) ])
    return f'SELECT {q_select} FROM {q_from} WHERE {q_where}'

def clear_tables(db):
    for t in TABLES:
        db.execute(f'TRUNCATE TABLE table_{t}')

def fill_tables(db, join_count, count):
    rng = default_rng()
    keys = np.int32(rng.choice(2**31, size=count, replace=False))

    for t in TABLES[:join_count]:
        new_keys = np.int32(rng.choice(2**31, size=count, replace=False))
        db.load_table(f'table_{t}', DataFrame({'key':keys, 'val':new_keys}))
        keys = new_keys
        np.random.shuffle(keys)

if __name__ == '__main__':
    join_count = 2
    if len(sys.argv) >= 2 and len(sys.argv[1]) > 0:
        join_count = int(sys.argv[1])
    
    repeat = 3
    if len(sys.argv) >= 3 and len(sys.argv[2]) > 0:
        repeat = int(sys.argv[2])

    main(join_count, repeat)