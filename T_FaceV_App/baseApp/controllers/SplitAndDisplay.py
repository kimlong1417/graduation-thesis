import cv2
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from baseApp.databases.models import Account, Image, Upload_Image


def display3chanels(request):
    upl1 = Upload_Image.objects.all()
    if request.method == "POST":
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        filenames = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.path(filenames)
        img_base64 = Image.objects.create(image=uploaded_file_url)
        img_base64.save()
        # img_0 = Upload_Image.objects.create(image=uploaded_file_url)
        # img_0.save()
        # upl = Image.objects.get(image=uploaded_file_url)
        img = cv2.imread(uploaded_file_url)
        # Lấy từng lớp ảnh
        img1 = img[:, :, 0]
        img2 = img[:, :, 1]
        img3 = img[:, :, 2]

        im1 = cv2.resize(img1,(200, 200))
        im2 = cv2.resize(img2,(200, 200))
        im3 = cv2.resize(img3,(200, 200))

        cv2.imwrite("D:\\Tai-Lieu-Hoc\\TNCKH\\Graduation_Thesis\\T_FaceV_App\\media1\\img1.jpg", im1)
        cv2.imwrite("D:\\Tai-Lieu-Hoc\\TNCKH\\Graduation_Thesis\\T_FaceV_App\\media1\\img2.jpg", im2)
        cv2.imwrite("D:\\Tai-Lieu-Hoc\\TNCKH\\Graduation_Thesis\\T_FaceV_App\\media1\\img3.jpg", im3)

        # filenames1 = fs.save(img1.name, img1)
        # uploaded_file_url1 = fs.path(filenames1)
        #
        # filenames2 = fs.save(img2.name, img2)
        # uploaded_file_url2 = fs.path(filenames2)
        #
        # filenames3 = fs.save(img3.name, img3)
        # uploaded_file_url3 = fs.path(filenames3)

        # if Upload_Image.objects.exists(image='D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\img1.jpg'):
        #     img_1 = Upload_Image.objects.update(
        #         image='D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\img1.jpg')
        img_1 = Upload_Image.objects.update_or_create(image='D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\img1.jpg')
        # img_1.save()
        # img_11 = Upload_Image.objects.get(uploaded_file_url1)

        img_2 = Upload_Image.objects.update_or_create(image='D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\img2.jpg')
        # img_2.save()
        # img_22 = Upload_Image.objects.get(uploaded_file_url2)

        img_3 = Upload_Image.objects.update_or_create(image='D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\img3.jpg')
        # img_3.save()
        # img_33 = Upload_Image.objects.get(uploaded_file_url3)

        # img_4 = Upload_Image.objects.exists()
        # for it in upl1:
        #     if it.image.name != img_3
        #     it.image.name

    return render(request, "display3Channels.html", {'upl1': upl1})