# Blood Group Identification System

## Overview
The **Blood Group Identification System** is an innovative application that uses advanced machine learning and fingerprint analysis to predict a user's blood group. This non-invasive approach provides a quick and efficient alternative to traditional blood typing methods.

## Features
- **Fingerprint Upload**: Users can upload their fingerprint images for analysis.
- **AI-Powered Analysis**: The system uses a trained machine learning model to analyze fingerprint patterns and predict blood groups.
- **User Authentication**: Secure login and signup functionality for users.
- **Responsive Design**: The application is accessible on both desktop and mobile devices.
- **Team and Project Information**: Learn more about the project and the team behind it.

## Technology Stack
- **Frontend**:
  - HTML5, CSS3, JavaScript
  - Jinja2 Templates
- **Backend**:
  - Python Flask
  - Flask-Login for user authentication
  - Flask-SQLAlchemy for database management
- **Machine Learning**:
  - TensorFlow for model training and prediction
  - OpenCV for fingerprint image preprocessing
  - NumPy for numerical computations
- **Database**:
  - SQLite (or any SQL database supported by SQLAlchemy)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/blood-group-identification.git
   cd blood-group-identification
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   .\venv\Scripts\activate   # For Windows
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Usage
1. **Sign Up**: Create an account to access the system.
2. **Login**: Log in to your account.
3. **Upload Fingerprint**: Navigate to the upload page and upload your fingerprint image.
4. **View Results**: The system will analyze the fingerprint and display the predicted blood group.

## Project Structure
```
Blood_group_identification/
├── app.py                     # Main application entry point
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
├── templates/                 # HTML templates
│   ├── home.html              # Homepage
│   ├── aboutProject.html      # About Project page
│   ├── auth/                  # Authentication templates
│       ├── login.html         # Login page
│       ├── signup.html        # Signup page
├── static/                    # Static files (CSS, JS, images)
│   ├── style.css              # Main stylesheet
├── routes/                    # Flask route definitions
│   ├── auth_routes.py         # Authentication routes
│   ├── fingerprint_routes.py  # Fingerprint-related routes
├── src/                       # Source code
│   ├── fingerprint/           # Fingerprint-related utilities
│       ├── utils.py           # Helper functions for fingerprint processing
│   ├── auth/                  # Authentication models
│       ├── models.py          # User model and database setup
```

## Future Enhancements
- Add support for more advanced fingerprint analysis techniques.
- Integrate cloud storage for uploaded fingerprints.
- Improve the accuracy of the machine learning model.

## Contributors
- **KrishnaVardhan Reddy** - Project Lead & ML Engineer
- **Nagendra Babu** - Frontend Developer
- **Sravya** - Backend Developer

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.