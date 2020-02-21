import os
import boto3
# see https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html
# to use DynamoDB local include endpoint_url, to use dynamoDB web service, remove endpoint_url
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

def handler(event, context):
    
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    output = "id;review;sentiment;\n"

    items = table.scan()

    for item in items['Items']:
        output+=(item['id']+";"+item['review']+ ";" + item['classification']+ ";\n") 
        print(item)
    
    
    return {
        "statusCode": 200,
        "headers" : {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true',
            "Content-Type": "text/csv; charset=utf-8",
            "Content-disposition": "attachment; filename=sentiment.csv"
        },
        
        "body": output 
        }