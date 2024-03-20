import os
import cv2
import requests
from tensorflow import keras
from keras.models import load_model
import numpy as np
import boto3

# Tạo một session với AWS
session = boto3.Session(
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], 
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], 
    aws_session_token=os.environ['AWS_SESSION_TOKEN'],
    region_name=os.environ['AWS_REGION'])
# Khởi tạo một client của AWS S3
s3 = session.client('s3')

# Tên bucket và đường dẫn đến file ảnh trên bucket
os.system('cp /var/task/natural_disaster.h5 /tmp/natural_disaster.h5')

bucket_name = os.environ['BUCKET_NAME']
# Đường dẫn đến thư mục chứa model
MODEL_DIR = "/tmp/natural_disaster.h5"

# load the trained model from disk
print("[INFO] loading model and label binarizer...")
# Kiểm tra xem MODEL_DIR có tồn tại không
if os.path.exists(MODEL_DIR):
    # Load model từ thư mục MODEL_DIR
    model = load_model(MODEL_DIR)
    print("Model directory is found!")
else:
    print("Model directory is not found!")

CLASSES = ["Cyclone", "Earthquake", "Flood", "Wildfire"]

def predict(image):
    # Preprocess the image
    cv2_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2_image = cv2.resize(cv2_image, (224, 224))
    cv2_image = cv2_image.astype("float32")

    # Expand the image dimension for model compatibility
    image = np.expand_dims(cv2_image, axis=0)

    # Predict the class
    pred = model.predict(image)[0]
    predicted_class = CLASSES[np.argmax(pred)]
    return predicted_class

def main(event, context):
    # Your code here
    print("Processing S3 event:", event)
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Example usage of predict function
    image_path = "https://" + bucket_name + ".s3.amazonaws.com/" + object_key
    print("Image path: " + image_path)
    # Tải file ảnh từ bucket
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        image_data = response['Body'].read()

        # Đọc ảnh trực tiếp từ data đã tải
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)

        prediction = predict(image)
        print("Prediction:", prediction)

        # Kiểm tra xem ảnh đã được đọc thành công chưa
        if image is None:
            print("Failed to load the image.")

    except Exception as e:
        print("Error:", e)

    return {
        'statusCode': 200,
        'body': 'Function executed successfully'
    }
