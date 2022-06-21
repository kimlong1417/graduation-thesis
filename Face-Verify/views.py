import base64
import io
import os
from os import listdir

import numpy as np
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, request, flash, redirect, jsonify
from flask_login import login_required, current_user
from keras.models import load_model
from numpy import asarray
from scipy import spatial
from sklearn.metrics.pairwise import cosine_distances
from werkzeug.utils import secure_filename
from mtcnn.mtcnn import MTCNN
import json
from scipy.spatial import distance
import math
from numpy import load

from .models import Image

from PIL import Image as Image1

from . import ALLOWED_EXTENSIONS, db, UPLOAD_FOLDER

views = Blueprint('views', __name__)
MODEL = load_model('D:/Github/graduation-thesis/facenet_keras.h5')



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)


def create_path():
    path = UPLOAD_FOLDER + 'upload/' + 'user_' + str(current_user.id) + "/"
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    return path


def result_path():
    path = UPLOAD_FOLDER + 'result/' + 'user_' + str(current_user.id) + "/"
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
                file.save(path)
                if check_faceNull(path,filename):
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
                    os.remove(path)
            else:
                flash('Allowed image types are - png, jpg, jpeg, gif', category='error')
                return redirect(request.url)
        image_path = create_path()
        train_X = load_faces(image_path)
        np.savez_compressed('D:/Github/graduation-thesis/Face-Verify/friends_dataset.npz', train_X)
        data = 'D:/Github/graduation-thesis/Face-Verify/friends_dataset.npz'
        load_face_dataset(data)
    return render_template("upload.html", user=current_user)


@views.route('/verify', methods=['GET', 'POST'])
@login_required
def verify_image():
    if request.method == 'POST':
        imageA = request.files['file1']
        # imageB = request.files['file2']

        if imageA and allowed_file(imageA.filename):
            filename = secure_filename(imageA.filename)
            imageA_path = os.path.join(create_path(), filename)
            imageA.save(imageA_path)
            imageA_pixel, imageA_align = extract_face(imageA_path)
            newTrain_ImageA = list()
            imageA_embedding = get_embedding(MODEL, imageA_align)
            newTrain_ImageA.append(imageA_embedding)
            newTrain_ImageA = np.asarray(newTrain_ImageA)
            flash('The first image successfully uploaded', category='success')
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)

        # if imageB and allowed_file(imageB.filename):
        #     filename = secure_filename(imageB.filename)
        #     imageB_path = os.path.join(create_path(), filename)
        #     imageB.save(imageB_path)
        #     imageB_pixel = extract_face(imageB_path)
        #     newTrain_ImageB = list()
        #     imageB_embedding = get_embedding(MODEL, imageB_pixel)
        #     newTrain_ImageB.append(imageB_embedding)
        #     newTrain_ImageB = np.asarray(newTrain_ImageB)
        #     flash('The first image successfully uploaded', category='success')
        # else:
        #     flash('Allowed image types are - png, jpg, jpeg, gif')
        #     return redirect(request.url)

        # Img = Image.query.filter_by(user_id=current_user.id).order_by(Image.img).all()
        total = 0
        point = 0
        dataset = load('D://Github//graduation-thesis//Face-Verify//friends_dataset_embeddings.npz')
        newTraindataX = dataset['arr_0']


        for newTrain_Image in newTraindataX:
            # # print(im.img)
            # imageB_pixel, imageB_align = extract_face(im.img)
            newTrain_ImageB = list()
            # imageB_embedding = get_embedding(MODEL, imageB_align)
            newTrain_ImageB.append(newTrain_Image)
            newTrain_ImageB = np.asarray(newTrain_ImageB)

            cosine_distances_score = compare_images(newTrain_ImageA,newTrain_ImageB)

            # print(cosine_distances_score)
            point += 1
            total += cosine_distances_score

        mean = total/point

        title = str(current_user.first_name)
        fig = plt.figure(title,figsize=(5, 3), facecolor="#F3F1F5")
        if (mean > 0.5):
            plt.suptitle("TRUE: the result is " + title)
        else:
            plt.suptitle("FALSE: the result is not " + title)

        # plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
        # show first image
        ax1 = fig.add_subplot(1, 3, 1)
        ax1.title.set_text("Base image")
        img_base = plt.imread(imageA_path)
        plt.imshow(img_base, cmap=plt.cm.gray)
        plt.axis("off")
        # show the second image
        ax2 = fig.add_subplot(1, 3, 2)
        ax2.title.set_text("Detected face")
        plt.imshow(imageA_pixel, cmap=plt.cm.gray)
        plt.axis("off")
        # show the third image
        ax3 = fig.add_subplot(1, 3, 3)
        ax3.title.set_text("Aligned image")
        plt.xlabel(float(mean))
        plt.imshow(imageA_align, cmap=plt.cm.gray)
        plt.axis("off")
        # show the images
        plt.savefig(result_path() + title + '.jpg')
        plt.close()

        pic = current_user.first_name + '.jpg'
        img1 = Image1.open(os.path.join(result_path(), pic))
        data = io.BytesIO()
        img1.save(data, "JPEG")

        encode_image = base64.b64encode(data.getvalue())
        return render_template("verify.html", pic = encode_image.decode("UTF-8"), user=current_user, mean = float(mean))
    return render_template("verify.html", user=current_user)


def check_faceNull(path,filename):
    # load image from file
    image = Image1.open(path)
    # convert to RGB, if needed
    image = image.convert('RGB')
    # convert to array
    pixels = asarray(image)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    results = detector.detect_faces(pixels)
    if len(results) > 1:
        flash('There are more than one face in this image - ' + str(filename) + '!!!', category='error')
        return False
    elif len(results) <= 0:
        flash('This image ' + str(filename) + ' does not have any faces', category='error')
        return False
    else:
        return True


def alignment_procedure(img, left_eye, right_eye):
    # this function aligns given face in img based on left and right eye coordinates

    left_eye_x, left_eye_y = left_eye
    right_eye_x, right_eye_y = right_eye

    # -----------------------
    # find rotation direction

    if left_eye_y >= right_eye_y:
        point_3rd = (right_eye_x, left_eye_y)
        direction = -1  # rotate same direction to clock
    else:
        point_3rd = (left_eye_x, right_eye_y)
        direction = 1  # rotate inverse direction of clock

    # -----------------------
    # find length of triangle edges

    a = distance.euclidean(np.array(left_eye), np.array(point_3rd))
    b = distance.euclidean(np.array(right_eye), np.array(point_3rd))
    c = distance.euclidean(np.array(right_eye), np.array(left_eye))

    # -----------------------

    # apply cosine rule

    if b != 0 and c != 0:  # this multiplication causes division by zero in cos_a calculation

        cos_a = (b * b + c * c - a * a) / (2 * b * c)
        angle = np.arccos(cos_a)  # angle in radian
        angle = (angle * 180) / math.pi  # radian to degree

        # -----------------------
        # rotate base image

        if direction == -1:
            angle = 90 - angle

        img = Image1.fromarray(img)
        img = np.array(img.rotate(direction * angle))

    # -----------------------

    return img  # return img anyway


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

    # -----------------
    keypoints = result[0]["keypoints"]
    left_eye = keypoints["left_eye"]
    right_eye = keypoints["right_eye"]
    # ------------

    # extract the bouding box from the first face
    x1, y1, width, height = result[0]['box']
    # bug fix
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]

    alignment_img = alignment_procedure(face, left_eye, right_eye)

    # resize pixels to the model size
    image = Image1.fromarray(alignment_img)
    image = image.resize(required_size)
    face_array = asarray(image)
    return face, face_array


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

def load_face_dataset(path):
    data = np.load(path)
    trainX = data['arr_0']
    # convert each face in the train set to an embedding
    newTrainX = list()
    for face_pixels in trainX:
        embedding = get_embedding(MODEL, face_pixels)
        newTrainX.append(embedding)
    newTrainX = np.asarray(newTrainX)
    # save arrays to one file in compressed format
    np.savez_compressed('D:/Github/graduation-thesis/Face-Verify/friends_dataset_embeddings.npz', newTrainX)



def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

# load images and extract faces for all images in a directory
def load_faces(directory):
    faces = list()
    #enumerate files
    for filename in listdir(directory):
        # path
        path = directory + filename
        # get face
        x, face = extract_face(path)
        face = asarray(face)
        # store
        faces.append(face)
        aa = asarray(faces)
    return aa

def compare_images(imageA, imageB):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imageA, imageB)
    spicy = 1 - spatial.distance.cosine(imageA, imageB)
    imgB_T = imageB.T
    nump = imageA.dot(imgB_T)/ (np.linalg.norm(imageA, axis=1) * np.linalg.norm(imgB_T))
    skl = 1 - cosine_distances(imageA,imageB)
    # s = ssim(imageA, imageB)
    return skl

@views.route('/delete-image', methods=['POST'])
@login_required
def delete_image():
    image = json.loads(request.data)
    imgId = image['imgId']
    image = Image.query.get(imgId)
    if image:
        if image.user_id == current_user.id:
            os.remove(image.img)
            db.session.delete(image)
            db.session.commit()
    return jsonify({})
