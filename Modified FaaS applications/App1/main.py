# coding=utf-8
# """ImageResize Lambda function handler"""
import time
init_st = time.time() * 1000
# from __future__ import print_function

import boto3
from wand.image import Image

from resize import resize_image

init_ed = time.time() * 1000
def handle_resize(request):

    fun_st = time.time() * 1000
    # Obtain the bucket name and key for the event
    # bucket_name = event['Records'][0]['s3']['bucket']['name']
    import datetime
    tm_st = datetime.datetime.now()
    bucket_name = "bucketname1"
    # key_path = event['Records'][0]['s3']['object']['key']
    key_path = "1.jpeg"

    # Retrieve the S3 Object
    s3_connection = boto3.resource('s3',aws_access_key_id="XXXXX",
                                aws_secret_access_key="XXXXX",
                                region_name="us-west-1")
    s3_object = s3_connection.Object(bucket_name, key_path)

    response = s3_object.get()

    # Perform the resize operation
    with Image(blob=response['Body'].read()) as image:
        resized_image = resize_image(image, 400, 400)
        resized_data = resized_image.make_blob()

    # And finally, upload to the resize bucket the new image
    s3_resized_object = s3_connection.Object('bucketname2', key_path)
    print(s3_resized_object.put(Body=resized_data))
    # print(",functioStart:{},".format(tm_st))
    fun_ed = time.time() * 1000
    return ",InitStart:{},".format(init_st)+"InitEnd:{},".format(init_ed)+"functionStart:{},".format(fun_st)+"functionEnd:{},".format(fun_ed)


    # Finally remove, as the bucket is public and we don't want just anyone dumping the list of our files!
    # s3_object.delete()

# handle_resize("", "")