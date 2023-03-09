from heavyai import connect

con = connect(user="admin", password="HyperInteractive", host="mm_heavydb", dbname="heavyai")

print(con)

query = "SELECT depdelay, arrdelay FROM flights_2008_10k ORDER BY depdelay LIMIT 10"
df = con.select_ipc(query)

print(df.head())
