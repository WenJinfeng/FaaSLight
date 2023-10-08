# import time
# init_st = time.time() * 1000
import flask
import requests
# init_ed = time.time() * 1000



def getUserDetails(event, context):
    import datetime
    tm_st = datetime.datetime.now()
    # fun_st = time.time() * 1000
    user = requests.get('https://randomuser.me/api/').json()
    user = user['results'][0]
    user['generator'] = 'google-cloud-function'
    # print(user)
    # fun_ed = time.time() * 1000
    print(",functioStart:{},".format(tm_st))
    
    # return ",InitStart:{},".format(init_st)+"InitEnd:{},".format(init_ed)+"functionStart:{},".format(fun_st)+"functionEnd:{},".format(fun_ed)

# print(getUserDetails(""))