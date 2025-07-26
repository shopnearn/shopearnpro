aws dynamodb query --table-name Market_dev --key-condition-expression "pk = :name" --expression-attribute-values  '{":name":{"S":"Amazon DynamoDB"}}'

key='{"pk":{"S":"U#rabinovich"},"sk":{"S":"U#rabinovich"}}'
key='{"pk":{"S":"U#klava"},"sk":{"S":"U#klava"}}'
key='{"pk":{"S":"U#nicole"},"sk":{"S":"U#nicole"}}'

aws dynamodb get-item --table-name Market_dev --key $key

aws dynamodb scan --table-name Market_dev --profile shopearn-dev

aws dynamodb get-item --table-name Market_dev --key $key --profile shopearn-dev

aws dynamodb get-item --table-name Market_dev  --key '{"pk":{"S":"U#rabinovich"},"sk":{"S":"U#rabinovich"}}' --projection-expression 'ColorList' --profile shopearn-dev

aws dynamodb update-item --table-name Market_dev --key $key --update-expression "SET ColorList = :e" --expression-attribute-values '{":e":{"L":[]}}' --return-values UPDATED_NEW --profile shopearn-dev

aws dynamodb update-item --table-name Market_dev --key $key --update-expression "SET ColorList = list_append(ColorList, :e)" --expression-attribute-values '{":e":{"L":[{"S":"Red"}]}}' --return-values UPDATED_NEW --profile shopearn-dev

aws dynamodb update-item --table-name Market_dev --key $key --update-expression "SET ColorList = list_append(:e, ColorList)" --expression-attribute-values '{":e":{"L":[{"S":"Purple"}]}}' --return-values UPDATED_NEW --profile shopearn-dev

aws dynamodb update-item --table-name Market_dev --key $key --update-expression "SET a = :a, ColorList = list_append(:l, ColorList)" --expression-attribute-values '{":l":{"L":[{"S":"Pink"}]},":e":{"S":"Pink"}, ":a":{"N": "2"}}' --condition-expression "not contains(ColorList, :e)" --return-values UPDATED_NEW --profile shopearn-dev

aws dynamodb update-item --table-name Market_dev --key $key --update-expression "REMOVE ColorList[0]" --return-values UPDATED_NEW --profile shopearn-dev

aws dynamodb update-item --table-name Market_dev --key $key --update-expression "SET ColorList = :e" --expression-attribute-values '{":e":{"L":[]}}' --return-values UPDATED_NEW --profile shopearn-dev
