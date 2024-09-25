import json
import boto3
import datetime
from datetime import datetime

def lambda_handler(event, context):
        client = boto3.client('rds')
        now = datetime.now()
        date = now.strftime("%d-%m-%Y-%H-%M-%S")
        tagname = now.strftime("%d-%m-%Y")
        #print("date and time =", date)
        response = client.create_db_snapshot(
        DBSnapshotIdentifier='mydbinstance-{}'.format(date),
        DBInstanceIdentifier='mydbinstance',
        Tags=[
               {
                 'Key': 'backupon',
                 'Value': tagname
               },
             ]
        )
        #return (response);