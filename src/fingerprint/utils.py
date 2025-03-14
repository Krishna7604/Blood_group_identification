import os

from src.auth.models import Prediction
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

import cv2
import numpy as np
from tensorflow.keras.preprocessing import image

def is_binary_image(img):
    """Check if the image contains only two unique pixel values: 0 and 255 (binary)."""
    unique_pixels = np.unique(img)
    return len(unique_pixels) <= 2 and (0 in unique_pixels) and (255 in unique_pixels)
import cv2
import numpy as np
from tensorflow.keras.preprocessing import image

def is_binary_image(img):
    """Check if an image is already binary (only contains 0 and 255)."""
    unique_values = np.unique(img)
    return np.array_equal(unique_values, [0, 255]) or np.array_equal(unique_values, [255])

def preprocesss_image(file_path, target_size=(128, 128)):
    """Preprocesses an image: Resize, noise reduction, contrast enhancement, binarization, and return in 3D format."""
    try:
        # Load image in RGB format
        img = image.load_img(file_path, target_size=target_size, color_mode='rgb')
        img_array = image.img_to_array(img).astype(np.uint8)

        # Convert image to grayscale
        gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        # Apply Gaussian Blur for noise reduction
        blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) for contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_img = clahe.apply(blurred_img)

        # Check if the image is already binary
        if not is_binary_image(enhanced_img):
            # Sharpen the image before thresholding
            kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])
            sharpened = cv2.filter2D(enhanced_img, -1, kernel)

            # Apply adaptive thresholding for better binarization
            binary_img = cv2.adaptiveThreshold(
                sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
        else:
            binary_img = enhanced_img

        # Convert back to 3D (RGB format with same values across all 3 channels)
        binary_img_3d = cv2.merge([binary_img, binary_img, binary_img])

        # Normalize to [0, 1] for model input
        processed_img = np.expand_dims(binary_img_3d, axis=0)  # Add batch dimension

        return processed_img  # Shape: (1, 128, 128, 3)

    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def preprocess_image(file_path, target_size=(128, 128)):
    """Preprocesses an image: Resize, convert to grayscale, binarize if needed, and return in 3D format."""
    try:
        # Load image in RGB format
        img = image.load_img(file_path, target_size=target_size, color_mode='rgb')
        img_array = image.img_to_array(img).astype(np.uint8)

        # Convert image to grayscale
        gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        # Check if already binary
        if not is_binary_image(gray_img):
            # Sharpen the image before thresholding
            kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])
            sharpened = cv2.filter2D(gray_img, -1, kernel)
            # kernel = np.ones((3,3),np.uint8)
            # gradient = cv2.morphologyEx(sharpened, cv2.MORPH_OPEN, kernel)
            # # Convert to binary (black & white)
            _, binary_img = cv2.threshold(sharpened, 128, 255, cv2.THRESH_BINARY)
        else:
            binary_img = gray_img

        # Convert back to 3D (RGB format with same values across all 3 channels)
        binary_img_3d = cv2.merge([binary_img, binary_img, binary_img])

        # Normalize to [0, 1] for model input
        # processed_img = binary_img_3d.astype(np.float32) / 255.0
        processed_img = np.expand_dims(binary_img_3d, axis=0)  # Add batch dimension

        return processed_img  # Shape: (1, 128, 128, 3)
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def predict_blood_grooop(imgarr):
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'model92.h5')
        mo1 = load_model(model_path)
        predictions = mo1.predict(imgarr)
        blood_groups = ['A+', 'A-', 'AB+', 'AB-', 'B+', 'B-', 'O+', 'O-']
        
        # Get top 3 predictions
        top3_indices = np.argsort(predictions[0])[-3:][::-1]
        top3_predictions = [
            (blood_groups[idx], float(predictions[0][idx]))
            for idx in top3_indices
        ]
        
        return top3_predictions
    except Exception as e:
        print(e)
        raise ValueError("Failed to load the model")

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