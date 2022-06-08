# Commands

List of commands to deploy locally before deploying it on AWS ECR.

```
docker build -t hello-world .
docker run -p 9000:8080 hello-world  
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'      
```

### 1. Retrieve an authentication token and authenticate your Docker client to your registry.
Use the AWS CLI:

```
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 966100334301.dkr.ecr.ap-southeast-1.amazonaws.com
```
Note: if you receive an error using the AWS CLI, make sure that you have the latest version of the AWS CLI and Docker installed.

### 2. Build your Docker image using the following command. For information on building a Docker file from scratch, see the instructions here . You can skip this step if your image has already been built:

```
docker build -t tealeenergysavingsapp .
```
### 3. After the build is completed, tag your image so you can push the image to this repository:
```
docker tag tealeenergysavingsapp:latest 966100334301.dkr.ecr.ap-southeast-1.amazonaws.com/tealeenergysavingsapp:latest
```
### 4. Run the following command to push this image to your newly created AWS repository:

```
docker push 966100334301.dkr.ecr.ap-southeast-1.amazonaws.com/tealeenergysavingsapp:latest
```

