import time
init_st = time.time() * 1000
import numpy
init_ed = time.time() * 1000

def testfunctions(request):
    """clear"""
    fun_st = time.time() * 1000
    for i in range(1):
        for j in range(1):
            for k in range(2):
                s = numpy.array([[i, j, k], [k, j, i]])
                print(s)
    fun_ed = time.time() * 1000
    return ",InitStart:{},".format(init_st)+"InitEnd:{},".format(init_ed)+"functionStart:{},".format(fun_st)+"functionEnd:{},".format(fun_ed)

# testfunctions()

