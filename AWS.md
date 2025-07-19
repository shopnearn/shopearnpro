# Useful AWS commands

### List AWS profiles

    aws configure list-profiles

### List details of the AWS profile

    aws configure list

### Verify AWS powertools layer version

    aws lambda get-layer-version-by-arn --arn "arn:aws:lambda:us-east-1:017000801446:layer:AWSLambdaPowertoolsPythonV3-python313-x86_64:20" --profile shopnearn-dev

### copy data from bucket to directory

    aws s3 cp s3://your-bucket-name/filename.txt /path/to/destination

### create cloudfront function with kv store

    aws cloudfront create-key-value-store --name my-redirects
    
    aws cloudfront list-key-value-stores

    {"Updates": [{"Operation": "Upsert","Key": "locale:fr","Value": "/fr"},{"Operation": "Upsert","Key": "locale:es","Value": "/es"}]}

    aws cloudfront describe-key-value-store --id my-redirects --query "KeyValueStore.Metadata.Version" --output text

    aws cloudfront update-key-value-store-keys --id kvs-abc123 --if-match ABCDEF1234567890== --updates file://updates.json

    
    aws cloudfront update-function --name my-function --function-config '{"Comment": "uses KVS","Runtime": "cloudfront-js-1.0","KeyValueStoreAssociations": [{ "KeyValueStoreARN": "arn:aws:cloudfront::<account-id>:key-value-store/my-redirects" }]}'--function-code file://index.js --stage DEVELOPMENT

    aws cloudfront list-functions --profile shopnearn-dev

resources:
Resources:
    CFKeyValueStore:
      Type: AWS::CloudFront::KeyValueStore
      Properties:
        Name: my-cloudfront-kvs-demo
    MyCloudFrontFunction:
      Type: AWS::CloudFront::Function
      Properties:
        Name: myCloudFrontFunction
        AutoPublish: true
        FunctionCode: |
            import cf from 'cloudfront';
            const kvsHandle = cf.kvs();
            async function handler(event) {
                const request = event.request;
                // Use the first segment of the pathname as key
                // For example http(s)://domain/<key>/something/else
                const pathSegments = request.uri.split('/')
                const key = pathSegments[1]
                try {
                    // Replace the first path of the pathname with the value of the key
                    // For example http(s)://domain/<value>/something/else
                    pathSegments[1] = await kvsHandle.get(key);
                    const newUri = pathSegments.join('/');
                    console.log(`${request.uri} -> ${newUri}`)
                    request.uri = newUri;
                } catch (err) {
                    // No change to the pathname if the key is not found
                    console.log(`${request.uri} | ${err}`);
                }
                return request;
            }
        FunctionConfig:
          Comment: CloudFront Function using KVS
          Runtime: cloudfront-js-1.0
        KeyValueStoreAssociations:
          - KeyValueStoreARN: !GetAtt CFKeyValueStore.Arn


service: cloudfront-kvs-demo

provider:
name: aws
region: us-east-1
runtime: nodejs18.x

resources:
Resources:

    MyKeyValueStore:
      Type: AWS::CloudFront::KeyValueStore
      Properties:
        Name: my-kvs-demo

    MyCloudFrontFunction:
      Type: AWS::CloudFront::Function
      Properties:
        Name: my-function-with-kvs
        AutoPublish: true
        FunctionConfig:
          Comment: Function with KVS lookup
          Runtime: cloudfront-js-1.0
        FunctionCode: |
          function handler(event) {
            var kv = keyValueStore.get("redirect:/fr");
            if (event.request.uri === "/fr") {
              return {
                statusCode: 302,
                statusDescription: "Found",
                headers: {
                  location: { value: kv || "/default" }
                }
              };
            }
            return event.request;
          }
        KeyValueStoreAssociations:
          - KeyValueStoreARN: !GetAtt MyKeyValueStore.Arn

    MyCloudFrontDistribution:
      Type: AWS::CloudFront::Distribution
      Properties:
        DistributionConfig:
          Enabled: true
          Comment: CloudFront with Function and KVS
          DefaultCacheBehavior:
            TargetOriginId: myOrigin
            ViewerProtocolPolicy: redirect-to-https
            AllowedMethods: [GET, HEAD]
            CachedMethods: [GET, HEAD]
            ForwardedValues:
              QueryString: false
              Cookies:
                Forward: none
            FunctionAssociations:
              - EventType: viewer-request
                FunctionARN: !GetAtt MyCloudFrontFunction.FunctionARN
          Origins:
            - Id: myOrigin
              DomainName: my-bucket.s3.amazonaws.com
              S3OriginConfig: {}


  MyBucket:
    Type: AWS::S3::Bucket

  MyCloudFrontOriginAccessControl:
    Type: AWS::CloudFront::OriginAccessControl
    Properties:
      OriginAccessControlConfig:
        Name: MyS3OriginAccessControl
        Description: Access control for S3 origin
        OriginAccessControlOriginType: s3
        SigningBehavior: always
        SigningProtocol: sigv4

  MyCloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Enabled: true
        DefaultRootObject: index.html
        Origins:
          - Id: S3Origin
            DomainName: !GetAtt MyBucket.RegionalDomainName
            S3OriginConfig: {}  # Required even if empty
            OriginAccessControlId: !Ref MyCloudFrontOriginAccessControl
        DefaultCacheBehavior:
          TargetOriginId: S3Origin
          ViewerProtocolPolicy: redirect-to-https
          AllowedMethods:
            - GET
            - HEAD
          CachedMethods:
            - GET
            - HEAD
          Compress: true
          ForwardedValues:
            QueryString: false
            Cookies:
              Forward: none
        ViewerCertificate:
          CloudFrontDefaultCertificate: true
