# Task_Sept_2024
Yaml
Create a Kubernetes Deployment named some-deployment to serve static files.

Requirements:
Labels:

The deployment should have two labels:
app = some-app
role = backend
Persistent Volume:

Application files are stored in a Persistent Volume Claim (PVC) named some-claim.
Use the storage class my-storage-class with ReadWriteOnce access mode for the PVC.
The PVC should be mounted to the application container as a volume named www and mounted at the path /usr/share/nginx/html.
Docker Image:

Use the official NGINX Docker image version 1.17.8-alpine.
Networking:

Expose the default HTTP port (80) and name the port http.
Health Checks:

Configure liveness and readiness probes:
Liveness probe:
Path: /health
Timeout: 5 seconds
Check interval: 10 seconds
Fail after 6 unsuccessful attempts
Initial delay: 10 seconds
Readiness probe:
Path: /ready
Timeout: 5 seconds
Check interval: 10 seconds
Initial delay: 15 seconds
Environment Variable:

The application container should have the environment variable APPLICATION_NAME set to some-app.
Execution Environment:

Assume the execution environment is Kubernetes version 1.17.




----------------------------------------------------------------------------------------------------------------------------------------------------------------



creat a notebook application. Your task is to implement an AWS Lambda function that will perform basic authentication and return the notes of the authenticated user. The notes and authentication data are stored in DynamoDB tables. The Lambda function is later exposed through the API Gateway and serves as an HTTP request handler. The runtime for the Lambda function is Python 3.8.

Notes:
The DynamoDB table holding the notes is named user-notes. Each note has the following attributes:

id (UUID v4)
user (the email of the owner)
create_date (the creation date, stored as a string in ISO_8601 format)
text (the actual note content)
Database Keys and Indexes:
The user-notes table consists of:

Partition key: user
Sort key: create_date
Authentication:
The DynamoDB table holding the authentication data is named token-email-lookup. The table has two fields:

token
email
Each authentication token maps to the email of the user owning the given token. The table has a partition key on the token field.

Authentication Header:
Tokens are passed to the Lambda function through the Authorization HTTP request header. The headers are available in event.headers. The authentication header value follows the Bearer token format.

To query the user-notes table using the user's email, you should first retrieve the email from the token-email-lookup table by reading the token from the HTTP request.

Requirements:
Finish the implementation of the provided Lambda function.
The function should return the user’s notes, sorted by the create_date attribute in descending order.
Return a maximum of 10 notes per query.
Return a 403 error status if the token is invalid or empty.
Return a 400 error status if the authentication header is malformed or missing.
