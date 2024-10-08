# RDS_snapshot_delete

1. I create  an RDS database using a cloud formation template. (In this template for the creation of the DB I didn't specify any values but I designed it to prompt the user to key in their desired variables from a list specified. Templates such as this one, can be reused and the list of values increased. variables can also be stored in the parameter store, which in my opinion, is the perfect option.)
 
 
![DBINSTANCE](https://github.com/user-attachments/assets/c7408bff-a46d-48f6-a3dd-d86588a7bdc7)


![cfdbinstance](https://github.com/user-attachments/assets/42676b79-1da3-4ce1-99ff-655aa3fe5dfd)


2. I created a lambda role with permission 
	AmazonRDSFullAccess
	AWSLambdaBasicExecutionRole (managed and not custom)
	AWSLambdaVPCAccessExecutionRole

 ![rdsrole](https://github.com/user-attachments/assets/5d8b0563-d15f-4877-8740-95f258af9a59)

3. Then I created a lambda function that will automate the creation of my database snapshots. I deployed my code and tested it successfully and a snapshot was created. This is a manual intervention that is prone to error. So we are going for all things  "automation".

![image](https://github.com/user-attachments/assets/08e2ab39-e372-4cc9-88e1-f9435c577a42)

![image](https://github.com/user-attachments/assets/8d1b7cef-bb0f-4e7e-b2cb-ea40f25ef575)

![image](https://github.com/user-attachments/assets/8e2cc026-e627-411a-9de0-f4799ec3bf43)



   

	
5. To automate snapshot creation, from the cloud watch tab,  Events > Rules> Create rule. Create a rule with a defined cron expression and schedule your rule to be triggered.  Cron expressions can be done according to your use case. In this demo I will have my function create a snapshot at 6 am, once triggered. I chose a flexible window of 5mins which means it can be created in that time frame.

![image](https://github.com/user-attachments/assets/87cc018f-c7f7-4763-932d-ffa982a66e1f)

![image](https://github.com/user-attachments/assets/f2c89084-2261-40f5-9dea-c589ec952b31)

   


5. select your target which is the lambda function for snapshots creation.  (I chose the create a new role for this event. If you need to use a role ensure to add necessary permissions). Now wait for the scheduled trigger time and see that the RDS snapshot has been created automatically
   

![image](https://github.com/user-attachments/assets/23e6297c-5958-4b12-9788-f3bb720ecfcd)

 
	
6. Lastly create a cloudwatch event rule for deleting snapshots the same way as creating a snapshot rule so I followed steps 4 and 5 again. Here I have scheduled the date and time in such a way that the delete rule will be triggered every 3 hours from creation. Demonstration purposes only.

![deletesnapshot1](https://github.com/user-attachments/assets/daee59b3-8138-4540-baca-b5f4f73c4954)

Navigate to Schedules on the EventBridge console and see the schedules you created

![image](https://github.com/user-attachments/assets/482a9f54-0de0-415a-a5c4-17d96fab1ab9)


7. I created another function that will be triggered for the deletion of creates snapshots and I tested it successfully but for me to ensure that it did what I desired, I reduced the time to minutes before changing it again. And remember that in testing the delete code you have to ensure that the snapshot is not in the creation process. Refresh until it is created otherwise the delete function will surely fail. Due to slow network issues, I couldn't get the snapshot in the delete phase so I decided to check the logs, on the monitor tab on the lambda console and view Cloudwatch logs
	
![image](https://github.com/user-attachments/assets/e3bf4fb6-ce53-48ba-afbd-1da24a9b3224)

 ![image](https://github.com/user-attachments/assets/a669371a-d726-4805-a183-a42c402b5659)

 ![image](https://github.com/user-attachments/assets/3087468d-d0c4-454f-90e4-b4a086e21f82)

 ![image](https://github.com/user-attachments/assets/24e381d6-d920-4c93-9085-0e87f02c0c73)

8. Finally! The moment of truth!
   
   at 6 am- snapshot was created within the flexible window of 5 mins

![image](https://github.com/user-attachments/assets/9c02c091-cce4-4f0d-a188-e27783bb1449)



2hrs later...if you check the time stamp and the ID of the instance is the same as the one created hours ago

![image](https://github.com/user-attachments/assets/b352ba6b-9de1-47e7-9fa9-258ef60fd9a4)



Don't forget to stop your instance or delete that stack once done. We are paying only for what we use. 

aws cloudformation delete-stack --stack-name DBInstance --region eu-north-1

or you can use the console

![stack delete](https://github.com/user-attachments/assets/a24d511d-e6c1-42ce-af6d-fdafb394efe9)

	
.

	


