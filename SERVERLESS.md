# Useful Serverless Framework commands

### Deploy the serverless application (run from project root directory)
    serverless deploy --aws-profile shopnearn-dev --service=service-cart

## All the commands below are to be run from service-cart directory 

### Verify that the serverless configuration is valid and print it
    serverless print --aws-profile shopnearn-dev

### Show the endpoints of the service
    serverless info --aws-profile shopnearn-dev

### Package the serverless application ()
    serverless package --aws-profile shopnearn-dev

### Deploy the serverless application
    serverless deploy --aws-profile shopnearn-dev

### Check the list of deployed files
    serverless deploy list --aws-profile shopnearn-dev

### Check the versions of deployed lambda functions
    serverless deploy list functions --aws-profile shopnearn-dev

### Check the logs of a running lambda function in real time
    serverless logs --function=hello --aws-profile shopnearn-dev --tail

### Invoke a specific lambda function from command line
    serverless invoke --function myfunc --aws-profile shopnearn-dev

### Delete the serverless application 
    serverless remove --aws-profile shopnearn-dev

### Commands related to the requirements plugin
    serverless requirements clean --aws-profile shopnearn-dev
    serverless requirements install --aws-profile shopnearn-dev
    serverless requirements cleanCache --aws-profile shopnearn-dev
