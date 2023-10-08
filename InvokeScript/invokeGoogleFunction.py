import os

import time
import json

# google cloud function deploy command
# gcloud functions deploy XX --entry-point XX --runtime python37 --trigger-http --allow-unauthenticated 


def run_cmd(cmd):
    """
    The simplest way to run an external command
    """
    return os.popen(cmd).read()


def invoke_fun(func_name, req_para, output_file):
    tm_st = time.time() * 1000
    
    try:
    	# google function invoke command
        resp = run_cmd("gcloud functions call %s --data %s" % (func_name, req_para))
        tm_ed = time.time() * 1000
        print(resp)
        init_st = resp.split("InitStart:")[1].split(",InitEnd:")[0]
        init_ed = resp.split(",InitEnd:")[1].split(",functionStart:")[0]
        fun_st = resp.split(",functionStart:")[1].split(",functionEnd:")[0]
        fun_ed = resp.split(",functionEnd:")[1].split(",")[0]
        # print(tm_st)
        # print(init_st)
        # print(init_ed)
        # print(fun_st)
        # print(fun_ed)
        # print(tm_ed)


        
        print("the total time of request")
        print(tm_ed-tm_st)
        totalTime = tm_ed-tm_st
        
        if (float(init_st)-tm_st)<0:
            #is warm start
            print("prepare time")
            print(float(fun_st)-tm_st)
            prepareTime = float(fun_st)-tm_st
            print("init time")
            print("no")
            initTime=0
        else:
            print("prepare time")
            print(float(init_st)-tm_st)
            prepareTime = float(init_st)-tm_st
            print("init time")
            print(float(fun_st)-float(init_st))
            initTime = float(fun_st)-float(init_st)
        
        print("function execution time")
        print(float(fun_ed)-float(fun_st))
        funTime = float(fun_ed)-float(fun_st)
        print("from function start to request end")
        print(tm_ed-float(fun_st))
        exeResTime = tm_ed-float(fun_st)

        print("Function-Name:{}, End-to-end-Time:{}, Prepare-Time:{}, Init-Duration:{}, Function-Duration:{}, Exec-add-Response:{}".format(func_name,totalTime,prepareTime,initTime,funTime,exeResTime))

        with open(output_file,"a") as f:
            f.write("Function-Name:{}, End-to-end-Time:{}, Prepare-Time:{}, Init-Duration:{}, Function-Duration:{}, Exec-add-Response:{}".format(func_name,totalTime,prepareTime,initTime,funTime,exeResTime))
            f.write("\n")

        



    except Exception as e:
        print(e)
        

    

    # if not resp:
    #     resp="ERROR"


# event1= json.dumps("{\"name\": \"hhh\"}")
# event1= json.dumps("{}")
# output_file= "Result/GoogleApp1.txt"
# invoke_fun("requestsApp",event1,output_file)
# invoke_fun("requestsAppAfter", event1, output_file)



if __name__ == "__main__":

    fun_names = ["requestsApp", "requestsAppAfter"]

    output_file= "Result/GoogleApp1.txt"

    event1= json.dumps("{}")

    for i in range(50):
        print("---------")
        print(i)
        time.sleep(1800)
        try:
            invoke_fun(fun_names[0], event1, output_file)
            invoke_fun(fun_names[1], event1, output_file)
        except Exception as e:
            print(e)
        # warm startup
        for k in range(2):
            print(k)
            time.sleep(30)
            try:
                
                invoke_fun(fun_names[0], event1, output_file)
                invoke_fun(fun_names[1], event1, output_file)
            
            except Exception as e:
                print(e)








