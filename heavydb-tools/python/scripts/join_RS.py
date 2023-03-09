from heavyai import connect
from time import time

db = connect(user="admin", password="HyperInteractive", host="mm_heavydb", dbname="heavyai")

time_a = time()
res = db.select_ipc('SELECT table_R.key, table_R.val AS val_R, table_S.val AS val_S FROM table_R, table_S WHERE table_R.key=table_S.key')
time_b = time()

print(f'The join took {time_b-time_a}s')
print('Result')
print(res)
