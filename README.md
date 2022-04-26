# FlaskApp
This web application, created using Flask, takes in any string value and converts it into a QR code exported to an S3 bucket using an AWS API. The user can also download the QR code from that S3 bucket. Whose contents will be listed in the web app. The application needs an AWS Access Key ID and the Secret Access Key to access the S3 bucket.

**Uploading to S3**

I have built the program to take in a text box value at the click of a button from HTML and sent that to python using flask functionality. After that, python processes the information, and converts it into a QR code, which it saves in the main directory. Next, the program looks for that file in the directory, and using an upload class that utilizes the S3 API, it sends the file to the S3 bucket.

**Downloading from S3**

To the right of the text box and submit button lies a list of all contents in the S3 bucket. These update in real time as new elements in the bucket are conceived. Each element is its own link that triggers a GET response that redirects to a download function found in Flask. This function works similarly to the upload function using the same API.

**Hosting the Web App**

The web app is hosted on an EC2 instance that uses a Ubuntu AMI. I first created an instance, gave it a security group that allows SSH from only my IP but allows HTTP access for everyone, and associated it with an elastic IP. I then SSH connected using my ppk key generated through Putty and the elastic IP. I logged in using username= Ubuntu and added my python files using GitHub. Next, I install Apache2 and configure my files so that the server hosts my Flask QR application. 
There is a problem with permissions and my code with Ubuntu Linux, so on this server, users cannot upload and download any files, but they can view the S3 bucket’s contents. I have tried solving this with countless acquaintances and even people in the IT field to no avail. However, the code works just fine locally, and the S3 is still being used as listing the QR codes.

**AutoScaling and CloudWatch**

For the web app to be auto scalable, I created an AMI of the EC2 instance that hosts the website. Then I created a launch configuration using the AMI. After that, I make an auto scaling group that can scale up to 4 instances. To know when to add or remove instances according to demand, I used CloudWatch to monitor the CPU Utilization and decide to either Scale Up and Down every 200 seconds. I also set up my email to receive alerts of when this happens.

**Database**

To integrate a database, I have created a NoSQL table using amazon’s DynamoDB. The database has two attributes: ID and Value. I then modified my python code, so when the user uploads a file, it feeds into the database with an incremental ID and the clicked png’s value, such as ‘www.google.com.’

**How I expect QRapp to work**

The user connects to the web app to create a QR code and download it. So, they enter it into the text box and click submit. Then, the QR code gets generated and sent to an S3 bucket, which is dynamically listed on the web page. At the same time, the QR code value is logged in the DYnamoDB database. After that, the user clicks on the link associated with their desired code and the respective png file to start their download.
