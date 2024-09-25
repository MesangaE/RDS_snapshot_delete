import json
import boto3
from datetime import datetime
from datetime import timedelta

def lambda_handler(event, context):
        client = boto3.client('rds')
        now = datetime.now() - timedelta(hours=4)   #change the retention days as per your requirement.
        date = now.strftime("%d-%m-%Y")
        snapshots = client.describe_db_snapshots(DBInstanceIdentifier= 'mydbinstance', SnapshotType='manual')
        print("These are the snapshots {} here",snapshots['DBSnapshots'])
        for i in snapshots['DBSnapshots']:
            
            ID = i['DBSnapshotIdentifier']
            S_type = i['SnapshotType']
            S_date= i['SnapshotCreateTime']
            S_date = S_date.strftime("%d-%m-%Y")
            print("These are the snapshots here")
            print(ID, S_date)
            if S_type == "manual":
                if S_date == date:
                    client.delete_db_snapshot( DBSnapshotIdentifier= ID )
                    print("We have deleted the {} RDS Snapshot".format(ID))