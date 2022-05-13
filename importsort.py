import json
import os

def sortresult(fileinput,input_package, fileoutput):
    
    # fileinput = "log-numpy-right.log"
    result = []
    for line in open(fileinput):
        result.append(line)
    
    T = []
    for i in result:
        if not i in T:
            T.append(i)

    T_new = []
    #result after deduplication
    for line in T:
        lines = line.split('=')
        lines[0] = lines[0].split(".py")[0].replace(input_package+"/","").replace('/','.')
        if len(lines)>2:
            if not ".".join(lines[0:len(lines)-1]) in T_new:
                T_new.append(".".join(lines[0:len(lines)-1]))
            # for i in range(1,len(lines)-1):
            #     T_new.append(".".join(lines[0:i+1]))
        
    # for i in T_new:
    #     # print('sss')
    #     print(i)

    T_new.sort()
    w = open(fileoutput, 'w')
    for i in T_new:
        # i=i.replace('\n','')
        w.write(i)
        w.write('\n')
    w.close

if __name__ == "__main__":
    
    pass
