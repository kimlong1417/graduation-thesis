import os

from django.shortcuts import render, redirect
import numpy as np
import cv2
import base64
from baseApp.databases.models import FileUpload
from T_FaceV_App.settings import STATICFILES_DIRS
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from baseApp.databases.models import Account, Image
from baseApp.forms import DocumentForm
from baseApp.repositories.serializers import AccountSerializer, ImageSerializer


def chuyen_anh_sang_base(img):
    try:
        with open(img, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
    except:
        return None

    return encoded_string


def chuyen_base64_sang_anh(anh_base64):
    try:
        anh_base64 = np.fromstring(base64.b64decode(anh_base64), dtype=np.uint8)
        anh_base64 = cv2.imdecode(anh_base64, cv2.IMREAD_ANYCOLOR)
    except:
        return None
    return anh_base64
# @api_view(['POST'])

def getBase64_process(request):
    # Đọc ảnh từ client gửi lên

    if request.method == "POST":
        serializer = AccountSerializer(data=request.POST)
        if serializer.is_valid():
            facebase64 = serializer.data['username']
            # try:
            #     username = Account.objects.filter(username=username1).get(password=password1)
            # except Account.DoesNotExist:
            #     return Response('Wrong', status=status.HTTP_400_BAD_REQUEST)

    return str(facebase64)

#
def postBase64_process(request):
#     # image = chuyen_anh_sang_base(request)
#     if request.method == "POST":
#         serializer = ImageSerializer(data=request.POST)
#         if serializer.is_valid():
#             facebase64 = serializer.data['document']
#             image = chuyen_anh_sang_base(facebase64)
#             img_base64 = Image.objects.create(image_base64=image)
#             img_base64.save()
#         return redirect('Home')
    return Response('Wrong', status=status.HTTP_200_OK)


def Home(request):
    if request.method == "POST":
        list = []
        for uploaded_file in request.FILES.getlist('document'):
            fs = FileSystemStorage()
            filenames = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_url = fs.path(filenames)
            list.append(uploaded_file_url)
            img_base64 = Image.objects.create(image_base64=uploaded_file_url)
            img_base64.save()
    return render(request, "home.html", {})

# uploaded_file = request.FILES['document']
# image = os.path.join(STATICFILES_DIRS, uploaded_file)
# list = []  # myfile is the key of a multi value dictionary, values are the uploaded files
# for f in request.FILES.getlist('document'):  # myfile is the name of your html file button
# fs = FileSystemStorage()
# filenames = fs.save(f.name, f)
# uploaded_file_url = fs.url(f)
# list.append(uploaded_file_url)

# serializer = ImageSerializer(data=request.FILES['document'])
# if serializer.is_valid():
#     facebase64 = serializer.data['document']
# image = chuyen_anh_sang_base(uploaded_file)
# image = "asdfggh"
# print(uploaded_file.name)