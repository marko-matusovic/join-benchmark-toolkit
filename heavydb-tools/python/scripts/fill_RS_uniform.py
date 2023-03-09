from heavyai import connect
from pandas import DataFrame
import sys
import numpy as np
from numpy.random import default_rng

db = connect(user="admin", password="HyperInteractive", host="mm_heavydb", dbname="heavyai")

count = sys.argv[1]
exp = {
    'k': 1e3,
    'm': 1e6,
    'g': 1e9
}
if count[-1].lower() in exp:
    count = int(int(count[:-1]) * exp[count[-1].lower()])
else:
    count = int(count)


print(f'Generating {count} rows')
rng = default_rng()
keys = np.int32(rng.choice(2**31, size=count, replace=False))

data_r = rng.integers(-2**31, 2**31, size=count, dtype=np.int32)
data_s = rng.integers(-2**31, 2**31, size=count, dtype=np.int32)

print(f'Filling table R')

db.load_table('table_R', DataFrame({'key':keys, 'val':data_r}))

np.random.shuffle(keys)

print(f'Filling table S')
db.load_table('table_S', DataFrame({'key':keys, 'val':data_s}))

print('done')
