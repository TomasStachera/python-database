import psycopg2
import  sys

#Python script for write "2 table" tables (main + detail table) to posgresql databese from file.
#This file was generated with import script
#Usage: python export_pgsql.py  file_name
#file_name: imported file name path

#Select 3 global parameters
main_name="BCP_testprogram"  #Main table name
detail_name="BCP_programdetail"  # detai table name


database_name="taskbuster_db"
database_user="djangouser"
database_password="tomass"


def create_connection():
    """ create a database connection to postgresql database
    :return: Connection object or None
    """
    conn = None
    conn = psycopg2.connect(database=database_name, user=database_user, password=database_password, host="127.0.0.1", port="5432")
    print("Connect to database OK")
    return conn

def WriteMain(conn,file):
    global main_name
    cur=conn.cursor()
    lin=file.readline()
    cmd="INSERT INTO "
    cmd=cmd+ '"'+main_name+'"'
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
    cmd=cmd+'"'+main_name+'"'
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
    cmd=cmd+'"'+detail_name+'"'
    arr=GetSchema(conn,detail_name)
    cmd=cmd+" ("
    first=True
    for ax in arr:
        if first == False:
            cmd=cmd+","
        first=False
        cmd=cmd+'"'+ax+'"'
    
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
    cmd="SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_NAME= '"
    cmd=cmd+namex
    cmd=cmd+"'"
    cur.execute(cmd)
    idx=cur.fetchall()

    ret_arr=[]
    first=True
    for x in idx:
        if first == False:
            c=str(x)
            lf=c.find("'");
            lr=c.rfind("'");
            ret=c[lf+1:lr]
            ret_arr.append(ret)
        first=False

        
    return ret_arr

    


def main():
    global detail_name


    if len(sys.argv) !=2:
        print("Script must have 1 argument: Input file_path name. Currentlly has {} arguments".format(len(sys.argv)))
        return 0
    
    f = open(sys.argv[1], "r",encoding="utf-8")
    # create a database connection
    conn = create_connection()
    idx=WriteMain(conn,f)
    WriteDetail(conn,f,idx)
    f.close()
    print("Export to database from file : {} done".format(sys.argv[1]))
    conn.close()
 
 
if __name__ == '__main__':
    main()
