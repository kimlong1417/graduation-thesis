import os

import numpy as np
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user
from keras.models import load_model
from numpy import asarray
from scipy import spatial
from sklearn.metrics.pairwise import cosine_distances
from werkzeug.utils import secure_filename
from mtcnn.mtcnn import MTCNN

from .models import Image

from PIL import Image as Image1

from website import ALLOWED_EXTENSIONS, db, UPLOAD_FOLDER

views = Blueprint('views', __name__)
MODEL = load_model('D:/Github/graduation-thesis/facenet_keras.h5')


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
                # print(path)
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


@views.route('/verify', methods=['GET', 'POST'])
@login_required
def verify_image():
    if request.method == 'POST':
        imageA = request.file['file1']
        imageB = request.file['file2']
        print(imageA, imageB)
    return render_template("verify.html", user=current_user)


def extract_face(Image_File, required_size=(160, 160)):
    # load image from file
    image = Image1.open(Image_File)
    # convert to RGB, if needed
    image = image.convert('RGB')
    # convert to array
    pixels = asarray(image)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    result = detector.detect_faces(pixels)
    # extract the bouding box from the first face
    x1, y1, width, height = result[0]['box']
    # bug fix
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]
    # resize pixels to the model size
    image = Image1.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    return face_array


def get_embedding(model, face_pixels):
    # scale pixel values
    face_pixels = face_pixels.astype('float32')
    # standardize pixel values across channels (global)
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    # transform face into one sample
    samples = np.expand_dims(face_pixels, axis=0)
    # make prediction to get embedding
    yhat = model.predict(samples)
    return yhat[0]


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def compare_image(imgA, imgB, imgA_pixel, imgB_pixel, title):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imgA_pixel, imgB_pixel)
    spicy = 1 -spatial.distance.cosine(imgA_pixel, imgB_pixel)
    imgB_pixel_T = imgB_pixel.T
    nump = imgA_pixel.dot(imgB_pixel_T) / (np.linalg.norm(imgA_pixel, axis=1) * np.linalg.norm(imgB_pixel_T))
    skl = 1 - cosine_distances(imgA_pixel, imgB_pixel)
    # setup the figure
    fig = plt.figure(title)
    plt.suptitle("MSE: %.5f, Spicy: %.5f, Numpy: %.5f, Sklearn: %.5f" % (m, spicy, nump, skl))
    # show first image
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(imgA, cmap=plt.cm.gray)
    plt.axis("off")
    # show the second image
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(imgB, cmap=plt.cm.gray)
    plt.axis("off")
    # show the images
    plt.savefig(UPLOAD_FOLDER + title + '.jpg')
