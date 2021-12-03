import ssim as ssim
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from baseApp.databases.models import Image, Compare_Image
import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.metrics import structural_similarity as ssim

def compareImage(request):
    kq1 = Compare_Image.objects.all()
    if request.method == "POST":
        uploaded_file1 = request.FILES['document']
        uploaded_file2 = request.FILES['document1']
        uploaded_file3 = request.FILES['document2']
        fs = FileSystemStorage()
        filenames1 = fs.save(uploaded_file1.name, uploaded_file1)
        filenames2 = fs.save(uploaded_file2.name, uploaded_file2)
        filenames3 = fs.save(uploaded_file3.name, uploaded_file3)
        uploaded_file_url1 = fs.path(filenames1)
        uploaded_file_url2 = fs.path(filenames2)
        uploaded_file_url3 = fs.path(filenames3)
        img_1 = Image.objects.create(image=uploaded_file_url1)
        img_1.save()
        img_2 = Image.objects.create(image=uploaded_file_url2)
        img_2.save()
        img_3 = Image.objects.create(image=uploaded_file_url3)
        img_3.save()


        img_ori = cv2.imread(uploaded_file_url1)
        img_const = cv2.imread(uploaded_file_url2)
        img_different = cv2.imread(uploaded_file_url3)

        original = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
        contrast = cv2.cvtColor(img_const, cv2.COLOR_BGR2GRAY)
        shopped = cv2.cvtColor(img_different, cv2.COLOR_BGR2GRAY)

        # compare the images
        compare_images(original, original, "OriginalAndOriginal")
        compare_images(original, contrast, "OriginalAndContrast")
        compare_images(original, shopped, "OriginalAndPhotoshopped")

        imgCompare1 = Compare_Image.objects.update_or_create(
            image='D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\OriginalAndOriginal.jpg')
        imgCompare2 = Compare_Image.objects.update_or_create(
            image='D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\OriginalAndContrast.jpg')
        imgCompare3 = Compare_Image.objects.update_or_create(
            image='D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\OriginalAndPhotoshopped.jpg')
    return render(request, "compareImage.html", {'kq1':kq1})


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB)
	# setup the figure
	fig = plt.figure(title)
	plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
	# show first image
	ax = fig.add_subplot(1, 2, 1)
	plt.imshow(imageA, cmap = plt.cm.gray)
	plt.axis("off")
	# show the second image
	ax = fig.add_subplot(1, 2, 2)
	plt.imshow(imageB, cmap = plt.cm.gray)
	plt.axis("off")
	# show the images
	plt.savefig('D:\Tai-Lieu-Hoc\TNCKH\Graduation_Thesis\T_FaceV_App\media1\\'+title+'.jpg')


