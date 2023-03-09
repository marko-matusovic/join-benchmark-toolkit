from heavyai import connect
from pandas import DataFrame
import numpy as np

db = connect(user="admin", password="HyperInteractive", host="mm_heavydb", dbname="heavyai")

df = DataFrame({'key':np.int32([]), 'val':np.int32([])})
if 'table_P' not in db.get_tables():
    print('creating table P')
    db.create_table('table_P', df)
if 'table_R' not in db.get_tables():
    print('creating table R')
    db.create_table('table_R', df)
if 'table_S' not in db.get_tables():
    print('creating table S')
    db.create_table('table_S', df)
if 'table_T' not in db.get_tables():
    print('creating table T')
    db.create_table('table_T', df)
if 'table_U' not in db.get_tables():
    print('creating table U')
    db.create_table('table_U', df)

print('truncating tables')
db.execute('TRUNCATE TABLE table_P')
db.execute('TRUNCATE TABLE table_R')
db.execute('TRUNCATE TABLE table_S')
db.execute('TRUNCATE TABLE table_T')
db.execute('TRUNCATE TABLE table_U')

print('done')
