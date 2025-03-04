from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

fingerprint_bp = Blueprint('fingerprint', __name__)

@fingerprint_bp.route('/')
def home():
    return render_template('home.html')

@fingerprint_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        # Add your fingerprint processing logic here
        return render_template('fingerprint/result.html')
    return render_template('fingerprint/upload.html') 