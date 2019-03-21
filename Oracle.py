from cx_Oracle import *

PORT = 1521
IP = "192.168.10.25"
dsn = makedsn(IP, PORT, "jaseng")
con = connect("jaseng", "jaseng", dsn)

cur = con.cursor()

cur.execute("SELECT * FROM EHREMPMST WHERE DEPTCD = 'ASGB10'")
print(cur.fetchall())

cursor.close()
con.close()