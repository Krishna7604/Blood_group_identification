import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import cv2
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# Global variable to store the model for better performance
model = None

def load_blood_group_model():
    global model
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'model95.h5')
        model = load_model(model_path)
        return True
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return False

def is_binary_image(img):
    # Check if image has only two unique pixel values (0 and 255)
    unique_pixels = np.unique(img)
    return len(unique_pixels) <= 2 and (0 in unique_pixels) and (255 in unique_pixels)

def preprocess_image(file_path):
    try:
        # Load and preprocess using keras.preprocessing.image
        img = image.load_img(file_path, target_size=(206, 192), color_mode='grayscale')
        img_array = image.img_to_array(img)
        
        # Convert to numpy array for OpenCV processing
        img_array = img_array.astype(np.uint8)
        img_array = img_array[:,:,0]  # Get single channel as it's grayscale
        
        # Check if image is already binary
        if not is_binary_image(img_array):
            # Apply preprocessing for non-binary images
            kernel = np.array([[0, -1, 0],
                             [-1, 5, -1],
                             [0, -1, 0]])
            sharpened = cv2.filter2D(img_array, -1, kernel)
            _, img_array = cv2.threshold(sharpened, 150, 255, cv2.THRESH_BINARY)
        
        # Reshape and normalize for model input
        processed_img = img_array.reshape(1, 206, 192, 1)
        processed_img = processed_img / 255.0
        
        return processed_img
        
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")

def predict_blood_group(image_array):
    global model
    if model is None:
        if not load_blood_group_model():
            raise ValueError("Failed to load the model")
    
    # Make prediction
    prediction = model.predict(image_array)
    blood_groups = ['A+', 'A-', 'AB+', 'AB-', 'B+', 'B-', 'O+', 'O-']
    predicted_index = np.argmax(prediction[0])
    confidence = float(prediction[0][predicted_index])
    
    return blood_groups[predicted_index], confidence 