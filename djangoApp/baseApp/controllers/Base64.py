from django.shortcuts import render, redirect
from django.http import HttpResponse


import base64
import numpy as np
import cv2

from baseApp.databases.models import Images
from baseApp.repositories.serializers import ImageSerializer



# def home(request):
#     if request.method == "POST":
#         img = request.FILES.get('document')
#         try:
#             with open(img, "rb") as image_file:
#                 encoded_string = base64.b64encode(image_file.read())
#         except:
#             return None
#         acc = Images.objects.create(images=encoded_string)
#         acc.save()
#     return HttpResponse(, "home.html", {})

def home(request):
    if request.method == "POST":
        my_upload_filed = request.FILES['file'].read()
        encoded_string = base64.b64encode(my_upload_filed)
        f = open("demo.txt", "w")
        f.write(str(encoded_string))
        f.close()
        return HttpResponse(encoded_string)
    return render(request, "home.html")

def base64(request):
    if request.method == "POST":
        my_upload_filed = request.FILES['file'].read()
        try:
            anh_base64 = np.fromstring(base64.b64decode(my_upload_filed), dtype=np.uint8)
            anh_base64 = cv2.imdecode(anh_base64, cv2.IMREAD_ANYCOLOR)
        except:
            return None
        return HttpResponse(anh_base64)
    return render(request,"home.html")