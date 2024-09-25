# RDS_snapshot_delete

	1. I create  an RDS database using a cloudformation template.
	![cloudfdbinstance](https://github.com/user-attachments/assets/60342053-cc17-449d-9df2-e6cf1ef0a452)
 
![DBINSTANCE](https://github.com/user-attachments/assets/c7408bff-a46d-48f6-a3dd-d86588a7bdc7)

	2. I created a lambda role with permission 
	AmazonRDSFullAccess
	AWSLambdaBasicExecutionRole (managed and not custom)
	AWSLambdaVPCAccessExecutionRole
	![lrole2](https://github.com/user-attachments/assets/cf109de9-8372-4124-95a5-7cec98c0bce5)

	3. Then I created a lambda function that will create snapshots for my DB instances. If the code ran successfully you will see a snapshot of the DB instance created. This a manual achievement so we are not going to get excites because we are going for all things "Automation". 
 
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
	 DBSnapshotIdentifier='sudip-test-db-identifier-{}'.format(date),
	 DBInstanceIdentifier='sudip-test-db-identifier',
	 Tags=[
	 {
	 'Key': 'backupon',
	 'Value': tagname
	 },
	 ]
	 )
	 #return (response);

then i deployed the lamda function and tested 

  ![testedsnapshotcreationcodelambda](https://github.com/user-attachments/assets/effb767d-b0a2-45c5-b274-9a9515c08103)

		To automate the creation we will head straight to the cloud watch tab from  Events > Rules>create rule. Create a rule and define the cron expression which will shedule your rule to be triggered. This can fit into any scenario you just need to define the cron according to your uses case. In this case i decided to create a snapsot at 7am with a flexible window of 5mins which means it can create in that time frame.
	
	 select your target which is the lambda function for snapshots creation.  (I chose the create new role for this event. If you need to use a role ensure to add necessary permissions). Now wait for the scheduled trigger time and see that RDS snapshot has been created automatically
	
	
	 Now periodically we have to delete them also. Otherwise cost for these RDS snapshot will be on the rise. So come to lambda tab again and create a lambda function for deleting snapshot like same as creating snapshot function.
	
	Here I want to delete snapshots which are more than 4 hours old since this is for demonstration purposes only. So this rule was created at 3.04am and by 7.04am we are expecting this snapshot to be deleted

	import json
	import boto3
	from datetime import datetime
	from datetime import timedelta
	
	def lambda_handler(event, context):
	 client = boto3.client('rds')
	 now = datetime.now() - timedelta(days=4) #change the retention days as per your requirement.
	 date = now.strftime("%d-%m-%Y")
	 snapshots = client.describe_db_snapshots(DBInstanceIdentifier= 'sudip-test-db-identifier', SnapshotType='manual')
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
  
 Lastly create a cloudwatch event rule for deleting snapshot sameway like creating snapshot rule. Here I have scheduled the date and time in such way that the delete rule will be triggered on every saturday at 2pm for demonstration purposes only. I would like to save costs 


	![RULES](https://github.com/user-attachments/assets/1f8e598e-1fc2-4197-b100-a0fd6e8dd548)

