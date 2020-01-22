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
dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url='http://localhost:8000')

def create(event, context):
    data = json.loads(event['body'])
    if len(data.review) == 0:
        logging.error("review text is empty")
        raise Exception("Couldn't insert prediction result to db.")

    timestamp = str(datetime.utcnow().timestamp())

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'classification': data.sentiment,
        'created_at': timestamp,
        'review': data.review,
        'verified': True,
        'id': hashlib.sha256(data.review.encode()),
    }

    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
