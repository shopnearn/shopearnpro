# Install Serverless Framework
### Install NPM packages
    npm install -g serverless
### Install requirements plugin
    serverless plugin install -n serverless-python-requirements

# Useful NPM commands
### list packages
    npm list
# Useful AWS commands
### List AWS profiles
    aws configure list-profiles
### List details of the AWS profile
    aws configure list

# Useful Serverless Framework commands

### deploy the serverless application (run from project root directory)
    serverless deploy --aws-profile shopnearn-dev --service=service-cart

## all the commands below are to be run from service-cart directory 

### verify that the serverless configuration is valid and print it
    serverless print --aws-profile shopnearn-dev

### show the endpoints of the service
    serverless info --aws-profile shopnearn-dev

### package the serverless application ()
    serverless package --aws-profile shopnearn-dev

### deploy the serverless application
    serverless deploy --aws-profile shopnearn-dev

### check the list of deployed files
    serverless deploy list --aws-profile shopnearn-dev

### check the versions of deployed lambda functions
    serverless deploy list functions --aws-profile shopnearn-dev

### check the logs of a running lambda function in real time
    serverless logs --function=hello --aws-profile shopnearn-dev --tail

### invoke a specific lambda function from command line
    serverless invoke --function myfunc --aws-profile shopnearn-dev

### delete the serverless application 
    serverless remove --aws-profile shopnearn-dev

### commands related to the requirements plugin
    serverless requirements clean --aws-profile shopnearn-dev
    serverless requirements install --aws-profile shopnearn-dev
    serverless requirements cleanCache --aws-profile shopnearn-dev
