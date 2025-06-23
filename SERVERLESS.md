# Install Serverless Framework
### Install NPM packages
    npm install -g serverless


# Useful NPM commands
### list packages
    npm list
# Useful AWS commands
### List AWS profiles
    aws configure list-profiles
### List details of the AWS profile
    aws configure list

# Common Serverless Framework commands

serverless invoke local --function service-cart/hello --aws-profile shopnearn-dev

### deploy the serverless application 
    serverless deploy --aws-profile shopnearn-dev
    serverless deploy --aws-profile shopnearn-dev --service=service-cart

serverless print --aws-profile shopnearn-dev

serverless info --aws-profile shopnearn-dev

serverless package --aws-profile shopnearn-dev


serverless requirements clean --aws-profile shopnearn-dev
serverless requirements install --aws-profile shopnearn-dev
serverless requirements cleanCache --aws-profile shopnearn-dev

serverless deploy --aws-profile shopnearn-dev

serverless deploy function --function page --aws-profile shopnearn-dev

serverless remove --aws-profile shopnearn-dev

serverless deploy list --aws-profile shopnearn-dev

serverless deploy list functions --aws-profile shopnearn-dev

serverless logs --function=hello --aws-profile shopnearn-dev --tail

serverless invoke --function hello --aws-profile shopnearn-dev

