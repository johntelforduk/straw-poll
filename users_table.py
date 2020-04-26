# Simple DynamoDB table with 1 row per user.

import json
import boto3
import hashlib


def hash_it(plain_text: str) -> str:
    """Return a hashed version of the parm string. The hashed version uses the 16 hex digits only."""
    hashing_function = hashlib.md5()
    hashing_function.update(plain_text.encode('utf-8'))
    hashed = hashing_function.hexdigest()
    return hashed


class UsersTable:

    def __init__(self, table_name: str):
        """Set up access to the users table."""
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(table_name)

    # def purge(self):
    #     """Remove all items from the table."""
    #     # Based on this Gist, https://gist.github.com/Swalloow/9966d576a9aafff482eef6b59c222baa
    #     scan = self.table.scan(
    #         ProjectionExpression='#k',
    #         ExpressionAttributeNames={
    #             '#k': 'user_id'
    #         }
    #     )
    #     with self.table.batch_writer() as batch:
    #         for each in scan['Items']:
    #             batch.delete_item(Key=each)

    def put(self, user_id: str, value):
        """Insert row for parm user ID into table. If there existing row, update it.
        The value is JSON encoded. The value may be either a dict or list."""
        self.table.put_item(
            Item={'user_id': hash_it(plain_text=user_id),
                  'value': json.dumps(value)})          # Do JSON encoding of the value dict, to turn it into a string.

    def scan_values(self):
        """Return list of all rows in the table."""
        rows = self.table.scan()                        # Scan all of the data from the table.
        finished = []
        for each_row in rows['Items']:                  # Work through the items (not the metadata).
            raw_value = each_row['value']
            finished.append(json.loads(raw_value))      # Decode JSON back to dictionary.
        return finished
