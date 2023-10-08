import time
init_st = time.time() * 1000
import logging
import numpy as np
import pandas as pd


logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')

init_ed = time.time() * 1000

def lambda_handler(request):
    fun_st = time.time() * 1000
    logger.info('numpy version is {}'.format(np.__version__))
    lib_version = {'numpy': np.__version__, 'pandas': pd.__version__}

    sales = [{'account': 'Jones LLC', 'Jan': 150, 'Feb': 200, 'Mar': 140},
             {'account': 'Alpha Co', 'Jan': 200, 'Feb': 210, 'Mar': 215},
             {'account': 'Blue Inc', 'Jan': 50, 'Feb': 90, 'Mar': 95}]
    df = pd.DataFrame(sales)
    logger.info(df)
    print(df)
    fun_ed = time.time() * 1000
    return ",InitStart:{},".format(init_st)+"InitEnd:{},".format(init_ed)+"functionStart:{},".format(fun_st)+"functionEnd:{},".format(fun_ed)


# print(lambda_handler("sss","ss"))