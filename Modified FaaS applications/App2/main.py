import time
init_st = time.time() * 1000
import boto3
import  PIL
from AWSScout2.__main__ import main
init_ed = time.time() * 1000
def handler(request):
    fun_st = time.time() * 1000
    print("Lambda Module Example")
    fun_ed = time.time() * 1000
    return ",InitStart:{},".format(init_st)+"InitEnd:{},".format(init_ed)+"functionStart:{},".format(fun_st)+"functionEnd:{},".format(fun_ed)


# if __name__ == '__main__':
#     handler(event=None, context=None)