# import the connect method 
from mysql.connector import connect
 
# define a connection object
conn = connect(
      user = 'root',
      password = 'billes1234',
      host = 'localhost',
      database = 'NUC_DB')
 
print('A connection object has been created.')

cursor = conn.cursor()
cursor.execute("SELECT * FROM chassis_TB")
records = cursor.fetchall()
for row in records:
    print(row)
cursor.close()
 
# close the database connection
conn.close()