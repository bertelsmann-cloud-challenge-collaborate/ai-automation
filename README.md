# ai-automation


## To start using this project:

### Prerequis

- Node + npm

then in ai-automation folder:


```
npm install serverless --save-dev
npm install serverless-offline@next --save-dev
npm install serverless-s3-local --save-dev
npm install serverless-dynamodb-local --save-dev
```


in your .aws/credentials add a profile:


```
[s3local]
aws_access_key_id = S3RVER
aws_secret_access_key = S3RVER
```

Run the project:

sls offline start


Copy the index.html in the local bucket created:

```
aws s3 cp index.html s3://local-bucket/index.html --endpoint-url http://localhost:8000
```

Copy the app.js in the local bucket created:

```
aws s3 cp app.js s3://local-bucket/app.js --endpoint-url http://localhost:8000
```

On another terminal open the folder ai-project and run the docker-compose up to start the flask app

Now you can open a browser:
http://localhost:8000/local-bucket/index.html


For information, with dynamodb-local started, you can go to this URL: http://localhost:8100/shell:

you can paste it to scan the table and see what's inside the DB:

```
var params = {
    TableName: 'SentimentReview',
    
    ReturnConsumedCapacity: 'NONE', // optional (NONE | TOTAL | INDEXES)
};
dynamodb.scan(params, function(err, data) {
    if (err) ppJson(err); // an error occurred
    else ppJson(data); // successful response
});
```
