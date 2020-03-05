import sys

oc1="\\r\\n"
repl=",'\\r',chr(13)),'\\n',chr(10))"
#Script replace ocurence in string oc1 with replacement SQL command defined in repl
#Scripti has 2 input parameters: source file, output file
    

def FinfOcurence(file,out_f):
    global oc1,oc2
    cont=0
    for x in file:
        c=x.find(oc1)
        cont=cont+1
        command_line=""
        if c>0:
            temp_str=x[:c]
            temp_str2=x[c:]
            rx=temp_str.rfind("'")
            left_str=x[:rx]
            rx2=temp_str2.find("'")
            centr_str=x[rx:rx2+c+1]
            right_str=x[rx2+c+1:]
            command_line=left_str+"replace(replace("+centr_str+repl+right_str
        else:
            command_line=x
        out_f.write(command_line)    
        
 

def main():

    if len(sys.argv) !=3:
        print("Script must have 3 arguments: Input file and output file. Currentlly has {} arguments".format(len(sys.argv)))
        return 0
    
    f = open(sys.argv[1], "r",encoding="utf-8")
    of = open(sys.argv[2], "w",encoding="utf-8")
    FinfOcurence(f,of)
    f.close()
    of.close()
    print("Data was exported to file : {}".format(sys.argv[2]))
    
 
 
if __name__ == '__main__':
    main()
