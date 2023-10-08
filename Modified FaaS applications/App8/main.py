import time
init_st = time.time() * 1000
import PIL
import cv2
import numpy

init_ed = time.time() * 1000
def handler(request):
    fun_st = time.time() * 1000
    print("cv2")
    fun_ed = time.time() * 1000
    return ",InitStart:{},".format(init_st)+"InitEnd:{},".format(init_ed)+"functionStart:{},".format(fun_st)+"functionEnd:{},".format(fun_ed)

# handler("","")