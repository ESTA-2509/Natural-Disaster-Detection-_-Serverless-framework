import os
import cv2
from tensorflow import keras
from keras.models import load_model
import numpy as np

# Đường dẫn đến thư mục chứa model
MODEL_DIR = "/app/natural_disaster.model"

# load the trained model from disk
print("[INFO] loading model and label binarizer...")
# Kiểm tra xem MODEL_DIR có tồn tại không
if os.path.exists(MODEL_DIR):
    # Load model từ thư mục MODEL_DIR
    model = load_model(MODEL_DIR)
else:
    print("Model directory not found!")

CLASSES = ["Cyclone", "Earthquake", "Flood", "Wildfire"]

def predict(image):
    cv2_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    cv2_image = cv2.resize(cv2_image, (224, 224))
    cv2_image = cv2_image.astype("float32")
    
    pred = model.predict(np.expand_dims(cv2_image, axis=0))[0]
    return CLASSES[pred]

def main(event, context):
    # Your code here
    print("Processing S3 event:", event)
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Example usage of predict function
    image = cv2.imread(object_key)
    prediction = predict(image)
    print("Prediction:", prediction)

    return {
        'statusCode': 200,
        'body': 'Function executed successfully'
    }
