import os
import pathlib

from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from .models import Image, User

from website import ALLOWED_EXTENSIONS, db, UPLOAD_FOLDER

views = Blueprint('views', __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


def create_path():
    path = UPLOAD_FOLDER + '/upload_' + str(current_user.id) + '/'
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    return path


@views.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'files' not in request.files:
            flash('No file part.', category='error')
            return redirect(request.url)
        files = request.files.getlist("files")
        if files.index == '':
            flash('No image selected for uploading.', category='error')
            return redirect(request.url)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(create_path(), filename)
                print(path)
                file.save(path)
                # check_image_name = Image.query.filter_by(img=path).first()
                # check user image where current_user = current_user.id, where img=path
                user_image = Image.query.filter_by(user_id=current_user.id, img=path).first()
                if user_image:
                    flash('This image already exists.', category='error')
                else:
                    pic = Image(img=path, user_id=current_user.id)
                    db.session.add(pic)
                    db.session.commit()
                    flash('Image successfully uploaded', category='success')
            else:
                flash('Allowed image types are - png, jpg, jpeg, gif', category='error')
                return redirect(request.url)
    return render_template("upload.html", user=current_user)


@views.route('/verify')
@login_required
def verify_image():
    return render_template("verify.html", user=current_user)
