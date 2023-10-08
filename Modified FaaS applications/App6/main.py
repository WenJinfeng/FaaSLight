import time
init_st = time.time() * 1000
import numpy
import pandas
init_ed = time.time() * 1000

def handler(request):
	fun_st = time.time() * 1000
	print(numpy.zeros(1))
	print(numpy.ones(1))
	s = pandas.Series(numpy.random.randn(5), index=['a', 'b', 'c', 'd', 'e'])
	print(s)
	fun_ed = time.time() * 1000
	return ",InitStart:{},".format(init_st)+"InitEnd:{},".format(init_ed)+"functionStart:{},".format(fun_st)+"functionEnd:{},".format(fun_ed)


# handler("","")