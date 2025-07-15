# Useful Serverless Framework commands

### Deploy the serverless application (run from project root directory)
    serverless deploy --aws-profile shopnearn-dev --service=service-cart

## All the commands below are to be run from service-cart directory 

### Verify that the serverless configuration is valid and print it
    serverless print --aws-profile shopnearn-dev

### Show the endpoints of the service (with stack outputs)
    serverless info --aws-profile shopnearn-dev
    serverless info --aws-profile shopnearn-dev --verbose

### Package the serverless application ()
    serverless package --aws-profile shopnearn-dev

### Deploy the serverless application
    serverless deploy --aws-profile shopnearn-dev

### Deploy only a specific lambda function
    serverless deploy function --aws-profile shopnearn-dev --function view

### Only update the configuration for a specific lambda function
    serverless deploy function --aws-profile shopnearn-dev --update-config --function view

### Check the list of deployed files
    serverless deploy list --aws-profile shopnearn-dev

### Check the versions of deployed lambda functions
    serverless deploy list functions --aws-profile shopnearn-dev

### Check the logs of a running lambda function in real time
    serverless logs --aws-profile shopnearn-dev --function=view  --startTime 1h --tail --filter TOKEN

### Displays service-wide metrics for the past 24 hours
    serverless metrics --aws-profile shopnearn-dev

### Displays metrics for a specific lambda function
    serverless metrics --aws-profile shopnearn-dev --function=view

### Invoke a specific lambda function from command line
    serverless invoke --function dbinit --aws-profile shopnearn-dev

### Delete the serverless application 
    serverless remove --aws-profile shopnearn-dev

### Create custom domain
    serverless create_domain --aws-profile shopnearn-dev
    serverless delete_domain --aws-profile shopnearn-dev
    aws acm list-certificates --region us-east-1 --profile shopnearn-dev

### Commands related to the requirements plugin
    serverless requirements install --aws-profile shopnearn-dev
    serverless requirements clean --aws-profile shopnearn-dev
    serverless requirements cleanCache --aws-profile shopnearn-dev

### Auxiliary commands
    serverless usage --aws-profile shopnearn-dev
    serverless reconcile --aws-profile shopnearn-dev
