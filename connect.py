# import the connect method 
from mysql.connector import connect
 
# define a connection object
conn = connect(
      user = 'root',
      password = 'billes1234',
      host = 'localhost',
      database = 'NUC_DB')
 
print('A connection object has been created.')

def TBprint(table):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM "+table)
    records = cursor.fetchall()
    for row in records:
        print(row)
    cursor.close()

#set things in mysql --------
cursor = conn.cursor()
cursor.execute(
"UPDATE options "+
"SET multi=false"
)
cursor.close()
#---------------------

print("---CHASSIS------------------------------------------------------------")
TBprint("chassis")
print("---CELLULES-----------------------------------------------------------")
TBprint("cellules")
print("---OPTIONS------------------------------------------------------------")
TBprint("options")

# close the database connection
conn.close()