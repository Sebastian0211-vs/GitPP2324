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
cursor.execute("SELECT * from options")
options = cursor.fetchall()
cursor.close()
print(options)
for option in options:
    if option[6]:
        #---update to API
        multi = option[1] #-> %M150.2
        billes = option[2]
        temps =option[3]
        infini = option[5]
        if infini:
            choixmodebilles = False #-> %M105.3
            choixmodetemps = False #-> %M105.4
            choixmodeinfini = True #-> %M105.5
        elif temps > 0:
            choixmodebilles = True #-> %M105.3
            choixmodetemps = False #-> %M105.4
            choixmodeinfini = False #-> %M105.5

            if option[4] == "h":
                temps = option[3] *60*60*1000 # %MD500 / %MD502
            elif option[4] == "m":
                temps = option[3] *60*1000
            else:
                temps = option[3] *1000
        elif billes > 0:
            choixmodebilles = True #-> %M105.3
            choixmodetemps = False #-> %M105.4
            choixmodeinfini = False #-> %M105.5

            # billes -> %MW208 / %MW210
        else:
            choixmodebilles = False #-> %M105.3
            choixmodetemps = False #-> %M105.4
            choixmodeinfini = True #-> %M105.5
        #---------------
        cursor = conn.cursor()
        cursor.execute(
        "UPDATE options "+
        "SET changed = false"
        )
        cursor.close()
        print("updated to API")
    else:
        #---update from API
        multi = 0 # <- %M150.2
        billes = 0 # <- %MW208 / %MW210
        infini = 0 # <- %M105.5
        temps = 6000 # <- %MD500 / %MD502
        if temps > 60*60*1000:
            temps = temps // (60*60*1000)
            unite = "h"
        elif temps > 60*1000:
            temps = temps // (60*1000)  
            unite = "m"
        else:
            temps = temps // 1000
            unite ="s"
        #---------
        cursor = conn.cursor()
        cursor.execute(
        "UPDATE options "+
        f"SET multi = {multi}, billes = {billes}, infini = {infini}, temps = {temps}, unite = '{unite}' "
        )
        cursor.close()
        print("updated from API")
    #------------------------

print("---OPTIONS------------------------------------------------------------")
TBprint("options")

# close the database connection
conn.commit()
conn.close()