nextId A#id B#id C#id U#id

# Basic entities
    A#ULID - account
    B#ULID - bill (invoice)
    C#ULID - cart
    U#ULID - user
    I#ULID - item
    O#ULID - order
    P#ULID - product
    R#ULID - reward
    P#ULID - payment

## Example user id
U#01JZ10H7X367VB2NF4YQ973DHW
U#00000000000000000000000000
U#ZZZZZZZZZZZZZZZZZZZZZZZZZZ

I#0000000000
I#2000000000
I#9999999999

Fetch last 10 orders (objects of type O#) for a given user.
```json
{
    "TableName": "Market",
    "Limit": 10,
    "ConsistentRead": false,
    "Select": "ALL_ATTRIBUTES",
    "KeyConditionExpression": "pk = :k AND sk BETWEEN :s AND :e",
    "ExpressionAttributeValues": {
        ":k": {"S": "user@example.com"},
        ":s": {"S": "O#00000000000000000000000000"},
        ":e": {"S": "O#ZZZZZZZZZZZZZZZZZZZZZZZZZZ"}
    },
    "ScanIndexForward": false,
    "ReturnConsumedCapacity": "TOTAL"
}
```
