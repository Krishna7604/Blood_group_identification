from src import create_app, db
from src.fingerprint.utils import load_blood_group_model

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Load the model at startup
        if not load_blood_group_model():
            print("Warning: Failed to load the blood group prediction model!")
    app.run(debug=True) 