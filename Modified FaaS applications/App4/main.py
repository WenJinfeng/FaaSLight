import time
init_st = time.time() * 1000
import json
# from sklearn.externals import joblib
# import sklearn
import joblib

model_name = 'model_1669535764.5820951.joblib'
model = joblib.load(model_name)
init_ed = time.time() * 1000
def predict(event):
    import datetime
    tm_st = datetime.datetime.now()
    body = {
        "message": "OK",
    }

    if 'queryStringParameters' in event.keys():
        params = event['queryStringParameters']

        medInc = float(params['medInc']) / 100000
        houseAge = float(params['houseAge'])
        aveRooms = float(params['aveRooms'])
        aveBedrms = float(params['aveBedrms'])
        population = float(params['population'])
        aveOccup = float(params['aveOccup'])
        latitude = float(params['latitude'])
        longitude = float(params['longitude'])

        inputVector = [medInc, houseAge, aveRooms, aveBedrms, population, aveOccup, latitude, longitude]
        data = [inputVector]
        predictedPrice = model.predict(data)[0] * 100000 # convert to units of 1 USDs
        predictedPrice = round(predictedPrice, 2)
        body['predictedPrice'] = predictedPrice
    
    else:
        body['message'] = 'queryStringParameters not in event.'

    print(body['message'])

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": 'application/json',
            "Access-Control-Allow-Origin": "*"
        }
    }
    print(",functioStart:{},".format(tm_st))

    return response

def do_main(request):
    fun_st = time.time() * 1000
    event = {
        'queryStringParameters': {
            'medInc': 200000,
            'houseAge': 10,
            'aveRooms': 4,
            'aveBedrms': 1,
            'population': 800,
            'aveOccup': 3,
            'latitude': 37.54,
            'longitude': -121.72
        }
    }

    response = predict(event)
    body = json.loads(response['body'])
    print('Price:', body['predictedPrice'])
    fun_ed = time.time() * 1000
    return ",InitStart:{},".format(init_st)+"InitEnd:{},".format(init_ed)+"functionStart:{},".format(fun_st)+"functionEnd:{},".format(fun_ed)


    # with open('event.json', 'w') as event_file:
    #     event_file.write(json.dumps(event))
    

# do_main()