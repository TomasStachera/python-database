import sqlite3
from sqlite3 import Error
import  sys

#Python script for read "2 table" tables (main + detail table) from sqlite databese to file.
#This file next can be exported to other database with script export_sqlite (or other)
#Usage: python import_sqlite.py name file_name
#name: name of test or tutorials or ..
#file_name: exported file name path

#Select 3 global parameters
main_name="BCP_testprogram"  #Main table name
detail_name="BCP_programdetail"  # detai table name
glob_db_name=r"db.sqlite3"  #name of sqlite database

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn

def ReadTutorial(conn,file,name):
    cur = conn.cursor()
    global main_name
    retazec="SELECT * FROM "
    retazec=retazec+ main_name
    retazec=retazec+" WHERE name = '{}'".format(name)
    cur.execute(retazec)
    idx=cur.fetchall()
    if len(idx)==0 :
        print("NO data found for selected name: {}".format(name))
        return -1
    elif len(idx) > 1:
        print("More than 1 returned id with name:{}, ids number:{}".format(name,len(idx)))
        return -1
    else :
        strx=str(idx)
        ps=strx.find(',')
        psr=strx.rfind(')')
        strx=strx[ps+1:psr]
        file.write(strx)
        file.write("\n")
        ret=idx[0][0]
        return ret
    



def ReadTable(conn,file,table_name,idx):
    cur = conn.cursor()
    retazec="SELECT * FROM "
    retazec=retazec+table_name
    retazec=retazec+" WHERE name_id = {}".format(idx)
    cur.execute(retazec)
    rows=cur.fetchall()
    for row in rows:
        strx=str(row)
        ps=strx.find(',')
        psr=strx.rfind(',')
        strx=strx[ps+1:psr]
        file.write(strx)
        file.write("\n")



def main():
    global detail_name
    global glob_db_name
    database = glob_db_name

    if len(sys.argv) !=3:
        print("Script must have 2 arguments:  main_name and output file_path name. Currentlly has {} arguments".format(len(sys.argv)))
        return 0
    
    f = open(sys.argv[2], "w",encoding="utf-8")
    # create a database connection
    conn = create_connection(database)
    idx=ReadTutorial(conn,f,sys.argv[1])
    if idx >0 :
        ReadTable(conn,f,detail_name,idx)
        print("Download to file : {} done".format(sys.argv[2]))
    f.close()
    
 
 
if __name__ == '__main__':
    main()
