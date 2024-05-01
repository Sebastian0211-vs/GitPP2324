# import the connect method 
from mysql.connector import connect
 
# define a connection object
conn = connect(
      user = 'root',
      password = 'billes1234',
      host = 'localhost',
      database = 'nuc_db')
 
print('A connection object has been created.')

#get tables---------------------------
def TBprint(table):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM "+table)
    records = cursor.fetchall()
    for row in records:
        print(row)
    cursor.close()
#------------------------------

#Programme de priorité---------
cursor = conn.cursor()
cursor.execute("SELECT changed from options")
changed = cursor.fetchone()[0]
cursor.close()

if changed:
    #---update to API
    cursor = conn.cursor()
    cursor.execute(
    "UPDATE options "+
    "SET changed = false"
    )
    cursor.close()
else:
    #---update from API
    pass
#------------------------

print("---OPTIONS------------------------------------------------------------")
TBprint("options")

# close the database connection
conn.commit()
conn.close()