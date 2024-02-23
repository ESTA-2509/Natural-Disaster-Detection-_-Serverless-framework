from tensorflow import keras
from keras.models import load_model
import numpy as np
import cv2

MODEL_PATH = "natural_disaster.model"
CLASSES = ["Cyclone", "Earthquake", "Flood", "Wildfire"]

# load the trained model from disk
print("[INFO] loading model and label binarizer...")
model = load_model(MODEL_PATH)

def predict(image):
    cv2_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    cv2_image = cv2.resize(cv2_image, (224, 224))
    cv2_image = cv2_image.astype("float32")
    
    pred = model.predict(np.expand_dims(cv2_image, axis=0))[0]
    return CLASSES[pred]