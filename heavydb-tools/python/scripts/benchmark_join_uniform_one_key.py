from heavyai import connect
from pandas import DataFrame
import sys
import numpy as np
from numpy.random import default_rng
from time import time
from enum import Enum

TABLES = ['P', 'R', 'S', 'T', 'U']

class KEY_JOIN_TYPE(Enum):
    SINGLE = 1
    CHAIN = 2

class DATA_SKEWNESS(Enum):
    UNIFORM = 1

def main(join_count, repeat):
    db = connect(user="admin", password="HyperInteractive", host="mm_heavydb", dbname="heavyai")

    print('Running benchmark on uniform join.')
    print(f'For {join_count} tables: {", ".join(TABLES[:join_count])}')
    print(f'Repeating {repeat} times.')

    join_type = KEY_JOIN_TYPE.SINGLE
    data_skewness = DATA_SKEWNESS.UNIFORM

    query = build_query(join_count, join_type)

    print(f'With query:\n{query}')

    for count in ['1k', '10k', '100k', '1m', '10m']:
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

def build_query(join_count, join_type):
    q_from = ', '.join([ f'table_{t}' for t in TABLES[:join_count] ])
    if join_type == KEY_JOIN_TYPE.SINGLE:
        q_select = 'table_P.key AS key, ' + ', '.join([ f'table_{t}.val AS val_{t}' for t in TABLES[:join_count] ])
        q_where = ' AND '.join([ f'table_{TABLES[ti]}.key=table_{TABLES[ti+1]}.key' for ti in range(join_count-1) ])
    else if join_type == KEY_JOIN_TYPE.CHAIN:
        q_select = ', '.join([ f'table_{t}.key AS key_{t}, table_{t}.val AS val_{t}' for t in TABLES[:join_count] ])
        q_where = ' AND '.join([ f'table_{TABLES[ti]}.val=table_{TABLES[ti+1]}.key' for ti in range(join_count-1) ])
    else:
        return 'Error: no valid join_type mehtod specified'
    
    return f'SELECT {q_select} FROM {q_from} WHERE {q_where}'

def clear_tables(db):
    for t in TABLES:
        db.execute(f'TRUNCATE TABLE table_{t}')

def fill_tables(db, join_count, count, join_type, data_skewness):
    rng = default_rng()
    if join_type == KEY_JOIN_TYPE.SINGLE:
        keys = np.int32(rng.choice(2**31, size=count, replace=False))
        for t in TABLES[:join_count]:
            np.random.shuffle(keys)
            data = rng.integers(-2**31, 2**31, size=count, dtype=np.int32)
            db.load_table(f'table_{t}', DataFrame({'key':keys, 'val':data}))
    else if join_type == KEY_JOIN_TYPE.CHAIN:
        
    else:
        return 'Error: no valid join_type mehtod specified'

if __name__ == '__main__':
    join_count = 2
    if len(sys.argv) >= 2 and len(sys.argv[1]) > 0:
        join_count = int(sys.argv[1])
    
    repeat = 3
    if len(sys.argv) >= 3 and len(sys.argv[2]) > 0:
        repeat = int(sys.argv[2])

    main(join_count, repeat)