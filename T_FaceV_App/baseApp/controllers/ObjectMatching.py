from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from baseApp.databases.models import Image, Upload_Image, ObjectMatching_Image
import cv2
import numpy as np
from matplotlib import pyplot as plt

def objectmatching(request):
    kq1 = ObjectMatching_Image.objects.all()
    if request.method == "POST":
        uploaded_file1 = request.FILES['document']
        uploaded_file2 = request.FILES['document1']
        fs = FileSystemStorage()
        filenames1 = fs.save(uploaded_file1.name, uploaded_file1)
        filenames2 = fs.save(uploaded_file2.name, uploaded_file2)
        uploaded_file_url1 = fs.path(filenames1)
        uploaded_file_url2 = fs.path(filenames2)
        img_1 = Image.objects.create(image=uploaded_file_url1)
        img_1.save()
        img_2 = Image.objects.create(image=uploaded_file_url2)
        img_2.save()

        img_rgb = cv2.imread(uploaded_file_url1)
        template = cv2.imread(uploaded_file_url2, 0)
        kq = obMProcess(img_rgb,template)
        cv2.imwrite("D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\OMI.jpg", kq)
        imgOM = ObjectMatching_Image.objects.update_or_create(
            image='D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\OMI.jpg')
    return render(request, "ObjectMatching.html", {'kq1':kq1})

def obMProcess(img_rgb,template):

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    height, width = template.shape[::]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    plt.imshow(res, cmap='gray')

    threshold = 0.5  # For TM_CCOEFF_NORMED, larger values = good fit.

    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + width, pt[1] + height), (255, 0, 0), 1)

    return img_rgb