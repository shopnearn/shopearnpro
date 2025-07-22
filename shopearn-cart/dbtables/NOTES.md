### Row-level and attribute-level security configuration
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem"
      ],
      "Resource": [
        "arn:aws:dynamodb:*:*:table/MyTable"
      ],
      "Condition": {
        "ForAllValues:StringEquals": {
          "dynamodb:LeadingKeys": [
            "U#${cognito-identity.amazonaws.com:sub}"
          ],
          "dynamodb:Attributes": [
            "name",
            "profile",
            "phone",
            "addr"
          ]
        },
        "StringEqualsIfExists": {
          "dynamodb:Select": "SPECIFIC_ATTRIBUTES",
          "dynamodb:ReturnValues": [
            "NONE",
            "UPDATED_OLD",
            "UPDATED_NEW"
          ]
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:BatchGetItem"
      ],
      "Resource": [
        "arn:aws:dynamodb:*:*:table/MyTable"
      ],
      "Condition": {
        "ForAllValues:StringEquals": {
          "dynamodb:LeadingKeys": [
            "U#${cognito-identity.amazonaws.com:sub}#O",
            "U#${cognito-identity.amazonaws.com:sub}#R"
          ]
        }
      }
    }
  ]
}
```

Possible Leading Keys values:

    Policy Variable	Example Value
    ${www.amazon.com:user_id}	amzn1.account.AGJZDKHJKAUUSW6C44CHPEXAMPLE
    ${graph.facebook.com:id}	123456789
    ${accounts.google.com:sub}	123456789012345678901
