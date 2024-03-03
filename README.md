## Directory Structure

```txt
$
|- serverless.yml (Deploy machine learning model using Serverless framework)
|- Dockerfile
|- handler.py
|- natural_disaster.model/ (Machine learning model)
```

## Abstract

## Setup

1. AWS:
   - Create an AWS Account and User -> Save an access key.
   - Create the EC2 Container Registry (ECR) for pushing Docker image
2. Create serverless.yml
   - Service và App Name:
      service: Đây là tên của dự án serverless, được đặt là "myserverlessproject".
      app: Đây cũng là tên của dự án, trong trường hợp này là "myserverlessproject".
  - Sử dụng Dotenv:
      useDotenv: true: Điều này cho phép sử dụng tệp dotenv để quản lý biến môi trường.
  - Phiên bản Framework:
      frameworkVersion: "3": Đây là phiên bản framework serverless được sử dụng.
  - Nhà cung cấp (Provider):
      name: Đây là tên nhà cung cấp, trong trường hợp này là "aws".
      profile: Đây là tên của profile AWS được sử dụng để triển khai.
  - ECR (Amazon Elastic Container Registry):
      images: Cấu hình cho hình ảnh Docker sử dụng trong ECR.
      appimage: Đây là tên của hình ảnh Docker trong ECR, được sử dụng cho ứng dụng.
  - Functions:
      myserverlessproject: Định nghĩa một hàm Lambda với các thuộc tính sau:
      image: Sử dụng hình ảnh Docker đã được định nghĩa trong ECR.
      timeout: Thời gian tối đa mà hàm được phép chạy trước khi bị hủy bỏ, trong trường hợp này là 900 giây.
      memorySize: Kích thước bộ nhớ được cấp phát cho hàm, trong trường hợp này là 2048 MB.
      events: Định nghĩa sự kiện kích hoạt hàm, trong trường hợp này là sự kiện khi có một đối tượng được tạo trong bucket S3 có tiền tố là "disasters/".
4. Create handler.py
   - Add aws_access_key_id, aws_secret_access_key, region_name below 
        session = boto3.Session(
        aws_access_key_id='***********',
        aws_secret_access_key='*******************************',
        region_name='us-east-1'
        )
    - Add bucket_name (Which is defined in serverless.yml)
    - Add the model directory (Ex: "/var/task/natural_disaster.model")
    - Add the S3 URL for catching event when 1 image uploaded in the folder under S3 URL (# Example usage of predict function
    image_path = "https://myserverlessproject-serverlessdeploymentbucket.s3.amazonaws.com/" + object_key)
5. Create Dockerfile (Install libraries and copy handler.py, natural_disaster.model folder) 
6. Build Dockerfile and push Docker image to ECR:
  - Retrieve an authentication token and authenticate your Docker client to your registry.
  - Use the AWS CLI:

    aws ecr get-login-password --region [region] | docker login --username AWS --password-stdin [ID_AWS_Account].dkr.ecr.us-east-1.amazonaws.com
    
    Note: If you receive an error using the AWS CLI, make sure that you have the latest version of the AWS CLI and Docker installed.
    
  - Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here . You can skip this step if your image is already built:

    docker build -t natural-disaster-image .
    
  - After the build completes, tag your image so you can push the image to this repository:
    
    docker tag natural-disaster-image:latest [ID_AWS_Account].dkr.ecr.us-east-1.amazonaws.com/natural-disaster-image:latest

  - Run the following command to push this image to your newly created AWS repository:
    
    docker push [ID_AWS_Account].dkr.ecr.us-east-1.amazonaws.com/natural-disaster-image:latest
7. Deploy serverless
8. Try push image to S3 folder (using CLI or Postman)
9. Check log file in Cloud log
