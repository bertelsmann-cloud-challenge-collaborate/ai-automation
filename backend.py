import json
import logging
import os
import time
import hashlib
from datetime import datetime
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

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

    response = {
        "statusCode": 200,
        "body": json.dumps(data),
        "headers" : {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true',
        },
    }

    return response