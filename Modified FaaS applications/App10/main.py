import time
init_st = time.time() * 1000
import lightgbm as lgb
import numpy

init_ed = time.time() * 1000
def handler(request):
    fun_st = time.time() * 1000
    
    dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
    X = dataset[:, 0:8]
    Y = dataset[:, 8]

    bst = lgb.Booster(model_file='model.txt')
    Ypred = bst.predict(X)
    print(numpy.mean((Ypred>0.5)==(Y==1)))
    fun_ed = time.time() * 1000
    return ",InitStart:{},".format(init_st)+"InitEnd:{},".format(init_ed)+"functionStart:{},".format(fun_st)+"functionEnd:{},".format(fun_ed)


# handler()