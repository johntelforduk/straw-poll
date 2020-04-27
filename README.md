# Straw Poll
![status](https://img.shields.io/badge/status-ready%20to%20use-green)

Website to run a quick survey.

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

#### Poll design
Poll questions can be defined by changing the `poll.json` file.

#### To run it
```
python server.py
```
`-d` argument to send debug info to stdout.

`-cdn` argument to serve graphic images from [CDN](https://en.wikipedia.org/wiki/Content_delivery_network). Otherwise, graphics are served from static folder on server.

#### Attribution
All images obtained from [Wikimedia Commons](https://commons.wikimedia.org/) and used under the terms of their Creative Commons licenses).