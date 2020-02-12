import json
import logging
import os
import time
import hashlib
from datetime import datetime

import boto3
# see https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html
# to use DynamoDB local include endpoint_url, to use dynamoDB web service, remove endpoint_url
#dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8100', aws_access_key_id='DEFAULT_ACCESS_KEY', aws_secret_access_key='DEFAULT_SECRET' )
#client = boto3.client('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8100')

def handler(event, context):
    data = json.loads(event['body'])
    if len(data) != 2:
        logging.error("Error on review")
        raise Exception("Couldn't insert prediction result to db.")
    review = data["review"]
    sentiment = data["sentiment"]
    
    timestamp = str(datetime.utcnow().timestamp())

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    item = {
        'classification': sentiment,
        'created_at': timestamp,
        'review': review,
        'verified': True,
        'id': hashlib.md5(review.encode()).hexdigest(),
    }

    # # write the todo to the database
    table.put_item(Item=item)

    # # create a response
    # response = {
    #     "statusCode": 200,
    #     "body": json.dumps(item)
    # }
    response = {
        "statusCode": 200,
        "body": json.dumps(data)
    }

    return response


def csvhandler(event, context):
    
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    output = "id;review;sentiment;\n"

    items = table.scan()

    for item in items['Items']:
        output+=(item['id']+";"+item['review']+ ";" + item['classification']+ ";\n") 
        print(item)
    
    
    return {
        "statusCode": 200, 
        "Content-Type": "text/csv; charset=utf-8",
        "body": output 
        }   
