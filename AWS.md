# Useful AWS commands

### List AWS profiles
    aws configure list-profiles

### List details of the AWS profile
    aws configure list

### Verify AWS powertools layer version
    aws lambda get-layer-version-by-arn --arn "arn:aws:lambda:us-east-1:017000801446:layer:AWSLambdaPowertoolsPythonV3-python313-x86_64:20" --profile shopnearn-dev

### copy data from bucket to directory
    aws s3 cp s3://your-bucket-name/filename.txt /path/to/destination
