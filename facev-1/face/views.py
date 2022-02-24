from django.shortcuts import render, redirect
from django.http import HttpResponse
from matplotlib.style import context
from .models import AccountUser, ImageUser
import uuid
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
    if(request.POST):
        login_data = request.POST.dict()
        username = login_data.get('username')
        password = login_data.get('password')
        try:
            pwd = uuid.uuid5(uuid.NAMESPACE_DNS,password)
            AccountUser.objects.filter(username=username).get(password=pwd)
        except AccountUser.DoesNotExist:
            return HttpResponse("Wrong username or password")
        # context = {username, password}
        # return HttpResponse(context)
        return render(request, 'index.html')
    return render(request, 'login.html')

def register(request):
    if(request.POST):
        register_data = request.POST.dict()
        username = register_data.get('username')
        email = register_data.get('email')
        password = register_data.get('password')
        cofirmPwd = register_data.get('cofirmPwd')
        if(password != cofirmPwd):
            return HttpResponse("Wrong username or password!")
        pwd = uuid.uuid5(uuid.NAMESPACE_DNS,password)
        account = AccountUser.objects.create(username=username,email=email,password=pwd)
        account.save()
        return HttpResponse("Successfully!")
    return render(request, 'register.html', {})

@login_required(login_url="/login/")
def test_view(request):
    context = {}
    return render(request, 'index.html', context)

def saveImage(request):
    if(request.POST):
        file = request.POST.dict()
        image = file.get('image')
        print(image)
        image_file = ImageUser.objects.create(image=image)
        image_file.save()
        return HttpResponse("Successfully!")
        