from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
import os
import PIL
import tempfile
import numpy as np
import base64
from werkzeug.utils import secure_filename
from src.fingerprint.utils import predict_blood_grooop
from src.fingerprint.utils import preprocess_image, predict_blood_group, load_blood_group_model
from src.auth.models import User, Prediction, db

fingerprint_bp = Blueprint('fingerprint', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}

BLOOD_COMPATIBILITY = {
    'A+': {'donate_to': ['A+', 'AB+'], 'receive_from': ['A+', 'A-', 'O+', 'O-']},
    'A-': {'donate_to': ['A+', 'A-', 'AB+', 'AB-'], 'receive_from': ['A-', 'O-']},
    'B+': {'donate_to': ['B+', 'AB+'], 'receive_from': ['B+', 'B-', 'O+', 'O-']},
    'B-': {'donate_to': ['B+', 'B-', 'AB+', 'AB-'], 'receive_from': ['B-', 'O-']},
    'AB+': {'donate_to': ['AB+'], 'receive_from': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']},
    'AB-': {'donate_to': ['AB+', 'AB-'], 'receive_from': ['A-', 'B-', 'AB-', 'O-']},
    'O+': {'donate_to': ['A+', 'B+', 'AB+', 'O+'], 'receive_from': ['O+', 'O-']},
    'O-': {'donate_to': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'], 'receive_from': ['O-']}
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@fingerprint_bp.route('/')
def home():
    return render_template('home.html')

@fingerprint_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('fingerprint/upload.html', 
                                 error_message='No file selected')
            
        file = request.files['file']
        if file.filename == '':
            return render_template('fingerprint/upload.html', 
                                 error_message='No file selected')
            
        if file and allowed_file(file.filename):
            try:
                # Update user information
                current_user.first_name = request.form.get('first_name')
                current_user.last_name = request.form.get('last_name')
                current_user.age = request.form.get('age')
                current_user.gender = request.form.get('gender')
                current_user.phone = request.form.get('phone')
                current_user.address = request.form.get('address')
                db.session.commit()

                temp_file = None
                try:
                    # Create temporary file
                    temp_file = tempfile.NamedTemporaryFile(suffix='.'+file.filename.rsplit('.', 1)[1].lower(), delete=False)
                    file.save(temp_file.name)
                    temp_file.close()  # Close the file before reading it again
                    
                    # Read and encode the image
                    with open(temp_file.name, "rb") as image_file:
                        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                    
                    # Process the image
                    processed_img = preprocess_image(temp_file.name)
                    
                    # Encode the processed image
                    try:
                        processed_img_pil = PIL.Image.fromarray(processed_img[0].astype(np.uint8))
                        buffered = "ecoded_imgg.png" #tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                        processed_img_pil.save(buffered, format="PNG")
                        
                        with open(buffered, "rb") as processed_image_file:
                            encoded_processed_image = base64.b64encode(processed_image_file.read()).decode('utf-8')
                    except Exception as e:
                        print(e)
                    # Get prediction
                    top3_predictions = predict_blood_grooop(processed_img)

                    # Save primary prediction to database
                    prediction = Prediction(
                        user_id=current_user.id,
                        blood_group=top3_predictions[0][0],
                        confidence=top3_predictions[0][1]
                    )
                    db.session.add(prediction)
                    db.session.commit()

                    return render_template('fingerprint/result.html',
                                          user=current_user,
                                          prediction=prediction,
                                          predictions=top3_predictions,
                                          blood_group=top3_predictions[0][0],
                                          confidence=top3_predictions[0][1],
                                          fingerprint_image=encoded_processed_image,
                                          processed_image=encoded_processed_image,
                                          donation_compatibility=BLOOD_COMPATIBILITY)
                                         
                except Exception as e:
                    if temp_file and os.path.exists(temp_file.name):
                        try:
                            os.unlink(temp_file.name)
                        except:
                            pass
                    raise e
                    
            except ValueError as ve:
                return render_template('fingerprint/upload.html', 
                                     error_message=f'Error processing image: {str(ve)}')
            except Exception as e:
                return render_template('fingerprint/upload.html', 
                                     error_message=f'Error processing request: {str(e)}')
                
        else:
            return render_template('fingerprint/upload.html', 
                                 error_message='Allowed file types are png, jpg, jpeg, bmp, tiff')
            
    return render_template('fingerprint/upload.html')

@fingerprint_bp.route('/about')
def about():
    return render_template('about.html')

@fingerprint_bp.route('/about-project')
def about_project():
    return render_template('aboutProject.html')