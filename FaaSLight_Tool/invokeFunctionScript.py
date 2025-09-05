
# each serverless application uses Serverless Framework to deploy to AWL Lambda
# see serverless.yml 

# use "serverless deploy" command

# after the deployment is successful, you can see the "name" of function that can be invoked


# in order to facilitate the processing of the results, we have written a script to invoke serverless applications
 
# it is as follows



import os
import datetime
import json
import boto3
import time
import base64

session = boto3.Session(aws_access_key_id="your aws_access_key_id",
                                aws_secret_access_key="your aws_secret_access_key",
                                region_name="your deployed region")
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
    tm_st = datetime.datetime.now()


    resp = client.invoke(FunctionName=fun_name,
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=json.dumps(event))

    # os.system("serverless invoke --function main --log")
    # os.system("ls")

    tm_ed = datetime.datetime.now()
   
    time.sleep(5)
    # print(base64.b64decode(resp['LogResult']))
    funStart = str(base64.b64decode(resp['LogResult'])).split(',functioStart:')[1].split(",")[0]
    duration = str(base64.b64decode(resp['LogResult'])).split('REPORT RequestId:')[1].replace("\\t", ",").split(",Duration:")[1].split(" ")[1]
    memory = str(base64.b64decode(resp['LogResult'])).split('REPORT RequestId:')[1].replace("\\t", ",").split(",Max Memory Used:")[1].split(" ")[1]
    bill = str(base64.b64decode(resp['LogResult'])).split('REPORT RequestId:')[1].replace("\\t", ",").split(",Billed Duration:")[1].split(" ")[1]
    

    initDuration = 0
    if ",Init Duration:" in str(base64.b64decode(resp['LogResult'])).split('REPORT RequestId:')[1].replace("\\t", ","):
        print("in")
        initDuration = str(base64.b64decode(resp['LogResult'])).split('REPORT RequestId:')[1].replace("\\t", ",").split(",Init Duration:")[1].split(" ")[1]
    addDuration = ""
 

    print("----")
    print(tm_st)
    print(funStart)
    print(tm_ed)
    tm_st = "{}".format(tm_st)
    tm_ed = "{}".format(tm_ed)
    print("---------------")
    print("Function-Name:{}, End-to-end-Time:{}, Arrive-Fun-Time:{}, Prepare-Time:{}, Init-Duration:{}, Function-Duration:{}{}, Billed-Duration:{}, Used-Memory:{}".format(fun_name,caltimeDelta(tm_st, tm_ed),caltimeDelta(tm_st, funStart),caltimeDelta(tm_st, funStart) - float(initDuration),initDuration,duration,addDuration,bill,memory))
    print("---------------")
    with open(output_file,"a") as f:
        if initDuration==0:
            f.write("Function-Name:{}, status:{}, End-to-end-Time:{}, Arrive-Fun-Time:{}, Prepare-Time:{}, Init-Duration:{}, Function-Duration:{}{}, Billed-Duration:{}, Used-Memory:{}".format(fun_name,"warm",caltimeDelta(tm_st, tm_ed),caltimeDelta(tm_st, funStart),caltimeDelta(tm_st, funStart) - float(initDuration),initDuration,duration,addDuration,bill,memory))
            f.write("\n")
        else:
            f.write("Function-Name:{}, status:{}, End-to-end-Time:{}, Arrive-Fun-Time:{}, Prepare-Time:{}, Init-Duration:{}, Function-Duration:{}{}, Billed-Duration:{}, Used-Memory:{}".format(fun_name,"cold",caltimeDelta(tm_st, tm_ed),caltimeDelta(tm_st, funStart),caltimeDelta(tm_st, funStart) - float(initDuration),initDuration,duration,addDuration,bill,memory))
            f.write("\n")
    f.close()






def exeAll(invokeLambda):

    #obtain the performance results of cold and warm starts    
    for fun_name in invokeLambda:
        print(fun_name)
        
        event = {}
        if fun_name in ["tensorflow-lambda-regression-before1","tensorflow-lambda-regression-after1","tensorflow-lambda-regression-after"]:
            event = {'queryStringParameters': {'x': 3.44}}
        if fun_name in ["boto3-before-dev-httpcheck","boto3-after1-dev-httpcheck","boto3-after-dev-httpcheck"]:
            event = {"ENDPOINT":"http://api.ipify.org?format=json",
            "METHOD":"GET",
            "TIMEOUT_MS":5,
            "REPORT_RESPONSE_BODY":"1",
            "REPORT_AS_CW_METRICS":"1",
            "CW_METRICS_NAMESPACE":"HttpCheckTestNamespace1",
            "BODY_REGEX_MATCH":"\\{\"ip\":(.*)\\}",
            "STATUS_CODE_MATCH": 200}
        if fun_name in ["wineML-before-dev-predict","wineML-after1-dev-predict","wineML-after-dev-predict"]:
            event = {"model name": "model-1028", 
            "fixed acidity": "7.4",
            "volatile acidity": "0.70",
            "citric acid": "0.00",
            "residual sugar": "1.9",
            "chlorides": "0.076",
            "free sulfur dioxide": "11.0",
            "total sulfur dioxide": "34.0",
            "density": "0.9978",
            "pH": "3.51",
            "sulphates": "0.56",
            "alcohol": "9.4"}
        if fun_name in ["housing-before-dev-predict-price", "housing-after1-dev-predict-price","housing-after-dev-predict-price"]:
            event = {
                'queryStringParameters': {
                    'medInc': 200000,
                    'houseAge': 10,
                    'aveRooms': 4,
                    'aveBedrms': 1,
                    'population': 800,
                    'aveOccup': 3,
                    'latitude': 37.54,
                    'longitude': -121.72}
                    }
        if fun_name in ["Bert-lambda-before", "Bert-lambda-after1", "Bert-lambda-after"]:
            event = {
                "body": "{\"context\":\"We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models (Peters et al., 2018a; Radford et al., 2018), BERT is designed to pretrain deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be finetuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial taskspecific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).\",\n\"question\":\"What is the GLUE score for Bert?\"\n}"
                }
        
        
        output_file = "Results/{}.txt".format(fun_name.split("-")[0])
        
        time.sleep(30)
        #cold start
        try:
            function_invoke_noinit(fun_name, event, output_file)
        except Exception as e:
            print(e)
        # warm start
        for k in range(2):
            time.sleep(30)
            try:
                function_invoke_noinit(fun_name, event, output_file)
            except Exception as e:
                print(e)





invokeLambda = [
    "HelloWorld-before-dev-main","HelloWorld-after1-dev-main","HelloWorld-after-dev-main",
    "Keras-TF-before", "Keras-TF-after1", "Keras-TF-after",
    "HelloPandas-before-dev-main","HelloPandas-after1-dev-main","HelloPandas-after-dev-main",
    "Opencv-before-dev-main","Opencv-after1-dev-main","Opencv-after-dev-main",
    "ResizeImage-before-dev-ResizeImage","ResizeImage-after1-dev-ResizeImage","ResizeImage-after-dev-ResizeImage",
    "tensorflow-lambda-regression-before1","tensorflow-lambda-regression-after1","tensorflow-lambda-regression-after",
    "Bert-lambda-before", "Bert-lambda-after1", "Bert-lambda-after",
    "Sentiment-predict-before-dev-main","Sentiment-predict-after1-dev-main","Sentiment-predict-after-dev-main",
    "lightGBM-before-dev-main","lightGBM-after1-dev-main","lightGBM-after-dev-main",
    "wineML-before-dev-train","wineML-after1-dev-train","wineML-after-dev-train",
    "wineML-before-dev-predict","wineML-after1-dev-predict","wineML-after-dev-predict",
    "PILOpenCV-before-dev-main","PILOpenCV-after1-dev-main","PILOpenCV-after-dev-main",
    "numpy-before-dev-main","numpy-after1-dev-main","numpy-after-dev-main",
    "lxmlrequests-before-dev-main","lxmlrequests-after1-dev-main","lxmlrequests-after-dev-main",
    "pandas-before-dev-main","pandas-after1-dev-main","pandas-after-dev-main",
    "skimage-before-dev-main","skimage-after1-dev-main","skimage-after-dev-main"
    ]

if __name__ == "__main__":

    for i in range(50):
        time.sleep(600)
        exeAll(invokeLambda)



  
