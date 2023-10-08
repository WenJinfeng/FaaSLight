# Google Cloud Functions Python Runtime Demo

Demo Google Cloud Function showing use of the Python 3 runtime.  [Read my tutorial on Medium](https://medium.com/@simon_prickett/writing-google-cloud-functions-with-python-3-49ac2e5c8cb3).

## Deployment

```
$ gcloud components update
$ gcloud components install beta
$ gcloud beta functions deploy getUserDetails --runtime python37 --trigger-http --project <projectId>
```

Where `<projectId>` is your Google Cloud project ID.

## Testing

Point a browser at:

```
https://<region>-<projectId>.cloudfunctions.net/getUserDetails
```

Where:

* `<region>` is the Google Cloud region that you deployed to (e.g. `us-central1`)
* `<projectId>` is your Google Cloud project ID

(the full URL that you need will be displayed in the output of the `gcloud` command when deploying the function).

You should see JSON representing a random user object pulled from the API that looks something like:

```
{
  "cell": "0911-857-4769", 
  "dob": {
    "age": 64, 
    "date": "1954-01-11T01:37:49Z"
  }, 
  "email": "محمدامين.پارسا@example.com", 
  "gender": "male", 
  "generator": "google-cloud-function", 
  "id": {
    "name": "", 
    "value": null
  }, 
  "location": {
    "city": "ایلام", 
    "coordinates": {
      "latitude": "32.1895", 
      "longitude": "-138.2377"
    }, 
    "postcode": 41995, 
    "state": "کرمانشاه", 
    "street": "206 دکتر مفتح", 
    "timezone": {
      "description": "Ekaterinburg, Islamabad, Karachi, Tashkent", 
      "offset": "+5:00"
    }
  }, 
  "login": {
    "md5": "c83471713279d94cb2a33a4b03a456cd", 
    "password": "lacrosse", 
    "salt": "B9vhBXeE", 
    "sha1": "09ff43c271437499467aab431df1bc522e1574a9", 
    "sha256": "f39c50bf339b6dd973e3dfdea0ddee451fc90cc5adb7580c8f386a2c9f2ff304", 
    "username": "orangeelephant750", 
    "uuid": "bcb042d5-7f52-47c1-b883-b296268bec07"
  }, 
  "name": {
    "first": "محمدامين", 
    "last": "پارسا"", 
    "title": "mr"
  }, 
  "nat": "IR", 
  "phone": "014-57870431", 
  "picture": {
    "large": "https://randomuser.me/api/portraits/men/40.jpg", 
    "medium": "https://randomuser.me/api/portraits/med/men/40.jpg", 
    "thumbnail": "https://randomuser.me/api/portraits/thumb/men/40.jpg"
  }, 
  "registered": {
    "age": 6, 
    "date": "2011-10-26T06:05:55Z"
  }
}
```