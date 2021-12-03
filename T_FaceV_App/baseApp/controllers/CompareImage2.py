import ssim as ssim
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from baseApp.databases.models import Image, Compare_Image, Compare_Image2
import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import structural_similarity as compare_ssim
import imutils


def compareImage2(request):
    kq1 = Compare_Image2.objects.all()
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


        imageA = cv2.imread(uploaded_file_url1)
        imageB = cv2.imread(uploaded_file_url2)

        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        (score, diff) = compare_ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")

        # threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255,
                               cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and then draw the
            # bounding box on both input images to represent where the two
            # images differ
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

        im1 = cv2.resize(imageA, (300, 300))
        im2 = cv2.resize(imageB, (300, 300))
        im3 = cv2.resize(diff, (300, 300))
        im4= cv2.resize(thresh, (300, 300))

        cv2.imwrite("D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\Original.jpg",im1)
        cv2.imwrite("D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\Modified.jpg", im2)
        cv2.imwrite("D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\Diff.jpg", im3)
        cv2.imwrite("D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\Thresh.jpg", im4)

        imgCompare1 = Compare_Image2.objects.update_or_create(
            image='D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\Original.jpg')
        imgCompare2 = Compare_Image2.objects.update_or_create(
            image='D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\Modified.jpg')
        imgCompare3 = Compare_Image2.objects.update_or_create(
            image='D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\Diff.jpg')
        imgCompare4 = Compare_Image2.objects.update_or_create(
            image='D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\Thresh.jpg')
    return render(request, "compareImage2.html", {'kq1':kq1})

