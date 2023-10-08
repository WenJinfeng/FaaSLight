import time
init_st = time.time() * 1000
import cv2
init_ed = time.time() * 1000

def lambda_handler(request):
    fun_st = time.time() * 1000
    print("OpenCV installed version:{}".format(cv2.__version__))
    print("It works!")
    fun_ed = time.time() * 1000
    return ",InitStart:{},".format(init_st)+"InitEnd:{},".format(init_ed)+"functionStart:{},".format(fun_st)+"functionEnd:{},".format(fun_ed)

    # return ("It works!")

# if __name__ == "__main__":
#     print(lambda_handler(42, 42))
