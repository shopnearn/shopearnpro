# DATABASE SCHEMA

The db schema below follows one table design principle, and currently consists of only ddb table: **Market.** The table has multi-tenant design, meaning that it is partitioned to allow multiple users securely co-exist in the same dataspace.

## Data Access Patterns

The following Access Patterns are defined for the application.

1. Get user profile
2. Get the list of last N orders for user
3. Display bonuses for user
4. Get a single order with all its items by id

## Database Index Schema

| Index     | Name          | PK | SK | Purpose                     | Notes  |
|-----------|---------------|----|----|-----------------------------|--------|
| Primary   | -             | pk | sk | lookup by user key, updates |        |
| Reverse   | ReverseIndex  | sk | pk | lookup by system key        |        |
| Id Lookup | IdLookupIndex | id | tp | lookup by business id       | sparse |

### Partition and System keys
PK stands for *Partition Key*, and SK for *System Key* (for the Primary index it also doubles as the *Sort Key*). *System Key* is a globally unique system identifier of an item, never visible to the end user. Each item can also have an optional business id (represented by *id* attribute), as well as the item type (the *tp* attribute). If both *id* and *tp* are present in the table, the item is projected to the IdLookupIndex and can be efficiently found via id lookup.
pk + sk combination is unique, with uniqueness enforced by the ddb table itself; thus, the sk + pk entries of the ReverseIndex are also unique, with strict one-to-one relationship to the Primary index.

### Primary index
This is the main ddb table index. Any updates to the table must be done using this index.

### Reverse index
This minimal index allows to lookup any item by its System Key. Note that this is a dense index and unique index that is guaranteed to have one-to-one correspondence with items in the main table. It does not affect writes, as no write (except delete) can affect the table's primary key.

### Id Lookup Index
This index allows lookups by an alternative id ("business id"), exposed to the user. This is sparse index, so not every item is obliged to have such an id, but the "important" entities, such as user, order, etc. should probably have it so that the item can be found without exposing its system id.

### Note on sparse indices
For a sparse index, only the values that have both of its PK and SK are projected into it. If an attribute for index's PK or SK is deleted in the main table, the corresponding record is also dropped from the sparse index. Thus, for a record to be projected into the IdIndex, both id and tp type need to be written to the item. 

### The *ttl* attribute
Any item that has the *ttl* attribute present, will be expired and subsequently removed from the table based on the timestamp contained in that attribute.

## Notes on data design

### Typed System Keys
Almost every system key in the data is a typed [ULID](https://github.com/ulid/spec/blob/master/README.md) id. ULIDs are chronologically sortable UUIDs which allows for data range queries against them. Normally, ULID has 26 characters from subset of English capital letters and digits ([A-Z0-9] - [ULIO]). Any System Key is composed of one-letter object type followed by ULID, separated by hash symbol (#). The following object types are defined:

| Type  | Entity         | Entity description        | ID suffix       |
|-------|----------------|---------------------------|-----------------|
| A     | account        | account (group of users)  | #ULID           |
| B     | bill           | order invoice or bill     | #ULID           |
| C     | cart           | user shopping cart        | #ULID           |
| I     | inventory item | inventory item or product | #ULID           |
| O     | order          | user order                | #ULID           |
| P     | payment        | payment record            | #ULID           |
| R     | reward         | reward transaction id     | #ULID           |
| U     | user           | user                      | #UUID (Cognito) |

Every system key will always be prefixed with type key as follows:

    U#550e8400-e29b-41d4-a716–446655440000
    A#01JZ10H7X367VB2NF4YQ973DHW
    O#01JZ10H7X367VB2NF4YQ973DHX
    R#01JZ10H7X367VB2NF4YQ973DHY

Note that U# keys use UUID instead of ULID because that's what Cognito provides as user identifier. Besides, there is no useful access pattern that would requre finding list of users by their creation time. 

### Notes on multi-shard design
The data in the Market table are partitioned by user key in multiple shards (that is, each user has a fixed number of well-defined partitions associated with the same user key), for example:

| Partition shard | Purpose       | Contains                       |
|-----------------|---------------|--------------------------------|
| U#rabinovich    | user profile  | addresses, phones, etc.        |
| U#rabinovich#O  | user orders   | all user orders by ulid        |
| U#rabinovich#P  | user products | all user products by ulid      |
| U#rabinovich#R  | user rewards  | all user bonus rewards by ulid |

Below is a sample data layout in the #O shard:

| PK             | SK                               | Contains       |
|----------------|----------------------------------|----------------|
| U#rabinovich#O | O#01JZ10H7X367VB2NF4YQ973DHW     | order metadata |
| U#rabinovich#O | O#01JZ10H7X367VB2NF4YQ973DHW#001 | order item 1   |
| U#rabinovich#O | O#01JZ10H7X367VB2NF4YQ973DHW#002 | order item 2   |
| U#rabinovich#O | O#01JZ10H7X367VB2NF4YQ973DHW#003 | order item 3   |
| U#rabinovich#O | O#01JZ10H7X367VB2NF4YQ973DXZ     | order metadata |
| U#rabinovich#O | O#01JZ10H7X367VB2NF4YQ973DXZ#001 | order item 1   |

The multi-shard design has the advantage of more precisely controlling the user access to its own data. For example, the profile shard can have read/write access pattern, whereas the Orders or Rewards shards can be read-only for the user, as they are updated asynchronously via a different process.

