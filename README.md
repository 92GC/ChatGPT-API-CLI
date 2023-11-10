# Running

Add a .env file to root of project with OPENAI_API_KEY=
Get the key from https://platform.openai.com/api-keys

Configure your AWS credentials by creating an IAM user in AWS Console, generating access keys, and setting them up on your local machine. Boto3 will use these credentials to access AWS services.

It should be part of group `full_users`

Store at `~/.aws/credentials`

create:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```



#### Run

`pip install boto3` (for AWS)

`pip install openai` (OpenAI)

# To do for back end
- replacing json with db
- unit test / e2e tests
- deploying to aws with teraform
- edit pdf with code
- map field name to box number and description
- concatenate and insert pages
- how to merge front and back end hooks
- handle box overflows

# To do for front end
- live update pdf in ui
- erase data in pdf
- upload pdf
- upload image
- download pdf
- running total of tax to pay
- move domain name to aws

## Dyanmo db notes
```
# Add an item (Put)
response = table.put_item(
   Item={
        'yourPrimaryKey': 'key1',
        'value': 123
    }
)

# Get an item (Get)
response = table.get_item(
    Key={
        'yourPrimaryKey': 'key1'
    }
)
item = response['Item']
print(item)

# Update an item
table.update_item(
    Key={
        'yourPrimaryKey': 'key1'
    },
    UpdateExpression='SET value = :val',
    ExpressionAttributeValues={
        ':val': 456
    }
)

# Delete an item
table.delete_item(
    Key={
        'yourPrimaryKey': 'key1'
    }
)
```