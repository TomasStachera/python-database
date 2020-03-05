import sqlite3
from sqlite3 import Error
import  sys

#Python script for write "2 table" tables (main + detail table) to sqlite databese from file.
#This file was generated with import script
#Usage: python export_sqlite.py  file_name
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

def WriteMain(conn,file):
    global main_name
    cur=conn.cursor()
    lin=file.readline()
    cmd="INSERT INTO "
    cmd=cmd+main_name
    arr=GetSchema(conn,main_name)
    cmd=cmd+" ("
    first=True
    for ax in arr:
        if first == False:
            cmd=cmd+","
        first=False
        cmd=cmd+ax
    
    cmd=cmd+ ") VALUES("
    cmd=cmd+lin[:-1]
    cmd=cmd+")"
    cur.execute(cmd)
    conn.commit()
    cmd="SELECT * FROM "
    cmd=cmd+main_name
    cmd=cmd+" ORDER BY id DESC LIMIT 1"
    cur.execute(cmd)
    idx=cur.fetchall()
    if len(idx)==0 :
        print("NO data found in database")
        return -1
    else:
        ret=idx[0][0]
        return ret

def WriteDetail(conn,file,idx):
    global detail_name
    cur=conn.cursor()
    cmd="INSERT INTO "
    cmd=cmd+detail_name
    arr=GetSchema(conn,detail_name)
    cmd=cmd+" ("
    first=True
    for ax in arr:
        if first == False:
            cmd=cmd+","
        first=False
        cmd=cmd+ax
    
    cmd=cmd+ ") VALUES("
    for x in file:
        ad_cmd=cmd
        ad_cmd=ad_cmd+x[:-1]
        ad_cmd=ad_cmd+","
        ad_cmd=ad_cmd+str(idx)
        ad_cmd=ad_cmd+")"
        cur.execute(ad_cmd)
        conn.commit()
        
            
            
        
        
def GetSchema(conn,namex):
    cur=conn.cursor()
    cmd="SELECT SQL from sqlite_master WHERE type='table' and name= '"
    cmd=cmd+namex
    cmd=cmd+"'"
    cur.execute(cmd)
    idx=cur.fetchall()
    retaz=str(idx[0])
    indx=retaz.find("PRIMARY KEY AUTOINCREMENT")+len("PRIMARY KEY AUTOINCREMENT")+1
    retaz=retaz[indx:]
    rex=retaz.split(',')
    ret_arr=[]
    for x in rex:
        ps=x.find('"')
        xpom=x[ps+1:]
        psr=xpom.find('"')
        if ps > -1 and psr >-1:
            strx=x[ps+1:psr+ps+1]
            ret_arr.append(strx)
    return ret_arr

    


def main():
    global detail_name
    global glob_db_name
    database = glob_db_name

    if len(sys.argv) !=2:
        print("Script must have 1 argument: Input file_path name. Currentlly has {} arguments".format(len(sys.argv)))
        return 0
    
    f = open(sys.argv[1], "r",encoding="utf-8")
    # create a database connection
    conn = create_connection(database)
    idx=WriteMain(conn,f)
    WriteDetail(conn,f,idx)
    f.close()
    print("Export to database from file : {} done".format(sys.argv[1]))
 
 
if __name__ == '__main__':
    main()
