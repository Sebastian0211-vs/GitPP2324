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

#set a variable to cell in SQL-----
cursor = conn.cursor()
cursor.execute("SELECT multi from options")
multi = cursor.fetchone()[0]
print(multi)
cursor.close()
#--------------------------------

#set things in mysql --------
cursor = conn.cursor()
cursor.execute(
"UPDATE options "+
"SET multi=false, unite ='h'"
)
cursor.close()
#---------------------

#----add line in mysql------------
#cursor =conn.cursor()
#cursor.execute(
#"INSERT INTO options (multi,billes,unite)"+
#"VALUES(false,31,'h')"
#)
#cursor.close()
#--------------------------



print("---CHASSIS------------------------------------------------------------")
TBprint("chassis")
print("---CELLULES-----------------------------------------------------------")
TBprint("cellules")
print("---OPTIONS------------------------------------------------------------")
TBprint("options")

# close the database connection
conn.commit()
conn.close()