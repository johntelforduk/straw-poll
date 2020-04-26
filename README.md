# Straw Poll
Website to take run a quick survey.

#### Installation
```
pip install flask
pip install wtforms
pip install boto3
pip install python-dotenv
```
See `requirements.txt` for details.

#### Credentials
The project needs a `.env` file like this,
```
# AWS
AWS_ACCESS_KEY_ID=<your access key>
AWS_SECRET_ACCESS_KEY=<your secret access key>
AWS_DEFAULT_REGION=<your region>
VOTES_TABLE=<your DynamoDB table name>
```