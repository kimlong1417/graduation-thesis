from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse

import base64

# Create your views here.

def home(request):
    if request.method == "POST":
        my_upload_filed = request.FILES['file'].read()
        encoded_string = base64.b64encode(my_upload_filed)
        return HttpResponse(encoded_string)
    return render(request, "home.html")