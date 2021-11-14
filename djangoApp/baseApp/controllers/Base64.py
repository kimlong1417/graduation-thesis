from django.shortcuts import render, redirect


import base64

from baseApp.databases.models import Images
from baseApp.repositories.serializers import ImageSerializer



def home(request):
    if request.method == "POST":
        serializer = ImageSerializer(data=request.POST)
        if serializer.is_valid():
            img = serializer.data['document']
            try:
                with open(img, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
            except:
                return None
            acc = Images.objects.create(images=encoded_string)
            acc.save()
    return render(request, "home.html", {})