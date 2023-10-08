import time
init_st = time.time() * 1000
import requests
from lxml import html
init_ed = time.time() * 1000
def handler(request):
    fun_st = time.time() * 1000
    url = "https://www.baidu.com/"
    response = requests.request("GET", url)
    # print(response.content)
    tree = html.fromstring(response.content)
    print(tree)
    fun_ed = time.time() * 1000
    return ",InitStart:{},".format(init_st)+"InitEnd:{},".format(init_ed)+"functionStart:{},".format(fun_st)+"functionEnd:{},".format(fun_ed)

 
# def handler():
#     url = "https://www.baidu.com/"
#     response = requests.request("GET", url)
#     print(response.content)
#     tree = html.fromstring(response.content)
#     print(tree)


# handler()