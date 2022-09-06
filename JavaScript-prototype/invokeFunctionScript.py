


import os
import datetime
import json
import boto3
import time
import base64

session = boto3.Session(aws_access_key_id="your aws_access_key_id",
                                aws_secret_access_key="your aws_secret_access_key",
                                region_name="us-west-1")
client = session.client(service_name='lambda')


def caltimeDelta(tm_st,tm_ed):
    #time interval processing

    tm_st_fen = tm_st.split(" ")[1].split(":")[1]

    tm_st_s = tm_st.split(" ")[1].split(":")[2].split(".")[0]
    tm_st_m = tm_st.split(" ")[1].split(":")[2].split(".")[1]

    tm_ed_fen = tm_ed.split(" ")[1].split(":")[1]
    tm_ed_s = tm_ed.split(" ")[1].split(":")[2].split(".")[0]
    tm_ed_m = tm_ed.split(" ")[1].split(":")[2].split(".")[1]

    timeDelta =(int(tm_ed_fen) - int(tm_st_fen))*60*1000 +(int(tm_ed_s)-int(tm_st_s))*1000+(int(tm_ed_m)-int(tm_st_m))/1000
    return timeDelta


 
def function_invoke_noinit(fun_name, event, output_file):

    # use function name and payload event to invoke the corresponding serverless function


    tm_st =time.time()
    # tm_st = datetime.datetime.now()


    resp = client.invoke(FunctionName=fun_name,
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=json.dumps(event))


    tm_ed = time.time()
   
  
    funStart = str(base64.b64decode(resp['LogResult'])).split(',functioStart:')[1].split(",")[0]
    duration = str(base64.b64decode(resp['LogResult'])).split('REPORT RequestId:')[1].replace("\\t", ",").split(",Duration:")[1].split(" ")[1]
    memory = str(base64.b64decode(resp['LogResult'])).split('REPORT RequestId:')[1].replace("\\t", ",").split(",Max Memory Used:")[1].split(" ")[1]
    bill = str(base64.b64decode(resp['LogResult'])).split('REPORT RequestId:')[1].replace("\\t", ",").split(",Billed Duration:")[1].split(" ")[1]
    

    initDuration = 0
    if ",Init Duration:" in str(base64.b64decode(resp['LogResult'])).split('REPORT RequestId:')[1].replace("\\t", ","):
        print("in")
        initDuration = str(base64.b64decode(resp['LogResult'])).split('REPORT RequestId:')[1].replace("\\t", ",").split(",Init Duration:")[1].split(" ")[1]
    addDuration = ""
 

    # print("----")
    # print(tm_st)
    # print(funStart)
    funStart=float(funStart)
    # print(tm_ed)

    print("---------------")

    with open(output_file,"a") as f:


        if initDuration==0:
            print("Function-Name:{}, status:{}, End-to-end-Time:{}, Arrive-Fun-Time:{}, Prepare-Time:{}, Init-Duration:{}, Function-Duration:{}{}, Billed-Duration:{}, Used-Memory:{}".format(fun_name,"warm",(tm_ed - tm_st)*1000,(funStart - tm_st*1000),(funStart - tm_st*1000) - float(initDuration),initDuration,duration,addDuration,bill,memory))
            f.write("Function-Name:{}, status:{}, End-to-end-Time:{}, Arrive-Fun-Time:{}, Prepare-Time:{}, Init-Duration:{}, Function-Duration:{}{}, Billed-Duration:{}, Used-Memory:{}".format(fun_name,"warm",(tm_ed - tm_st)*1000,(funStart - tm_st*1000),(funStart - tm_st*1000) - float(initDuration),initDuration,duration,addDuration,bill,memory))
            f.write("\n")

        else:
            print("Function-Name:{}, status:{}, End-to-end-Time:{}, Arrive-Fun-Time:{}, Prepare-Time:{}, Init-Duration:{}, Function-Duration:{}{}, Billed-Duration:{}, Used-Memory:{}".format(fun_name,"cold",(tm_ed - tm_st)*1000,(funStart - tm_st*1000),(funStart - tm_st*1000) - float(initDuration),initDuration,duration,addDuration,bill,memory))
            f.write("Function-Name:{}, status:{}, End-to-end-Time:{}, Arrive-Fun-Time:{}, Prepare-Time:{}, Init-Duration:{}, Function-Duration:{}{}, Billed-Duration:{}, Used-Memory:{}".format(fun_name,"cold",(tm_ed - tm_st)*1000,(funStart - tm_st*1000),(funStart - tm_st*1000) - float(initDuration),initDuration,duration,addDuration,bill,memory))
            f.write("\n")
    f.close()



# fun_name = "microcosm2rss-dev-microcosm"
# fun_name = "microcosm2rss-after-dev-microcosm"
# fun_name = "show-me-a-dog-dev-list"
# # fun_name = "show-me-a-dog-after-dev-list"
# fun_name = "aws-lunch-dev-menu"
# fun_name = "aws-lunch-after-dev-menu"
# fun_name = "image-processingS3-dev-processing"
# fun_name = "image-processingS3-after-dev-processing"

# # event1 ={"query":{"site": "https://espruino.microco.sm", "microcosm": "557"}}
# event1 = ""
# event1 = {"queryStringParameters": {"f":"1.jpeg","t":'jpeg'}};
# # function_invoke_noinit(fun_name, event1, "ExecutionResult/App1.txt")
# function_invoke_noinit(fun_name,event1, "ExecutionResult/App2.txt" )
# function_invoke_noinit(fun_name,event1, "ExecutionResult/App3.txt" )
# function_invoke_noinit(fun_name,event1, "ExecutionResult/App4.txt" )



if __name__ == "__main__":
    fun_names = ["image-processingS3-dev-processing", "image-processingS3-after-dev-processing"]

    output_file="ExecutionResult/App4.txt"

    # event = {"query":{"site": "https://espruino.microco.sm", "microcosm": "557"}}
    event = {"queryStringParameters": {"f":"1.jpeg","t":'jpeg'}}

    # function_invoke_noinit(fun_names[0], event, output_file)
    # function_invoke_noinit(fun_names[1], event, output_file)

    for i in range(50):
        print("---------")
        print(i)
        time.sleep(600)
        try:
            function_invoke_noinit(fun_names[0], event, output_file)
            function_invoke_noinit(fun_names[1], event, output_file)
        except Exception as e:
            print(e)
        # warm startup
        for k in range(2):
            print(k)
            time.sleep(30)
            try:
                
                function_invoke_noinit(fun_names[0], event, output_file)
                function_invoke_noinit(fun_names[1], event, output_file)
            
            except Exception as e:
                print(e)








