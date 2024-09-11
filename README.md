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
