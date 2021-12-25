from django.shortcuts import render
from django.http import HttpResponse
from .models import AccountUser
import uuid

# Create your views here.

def login(request):
    if(request.POST):
        login_data = request.POST.dict()
        username = login_data.get('username')
        password = login_data.get('password')
        try:
            pwd = uuid.uuid5(uuid.NAMESPACE_DNS,password)
            password1 = str(pwd)
            pwd1 = AccountUser.objects.filter(username=username).get(password=password1)
        except AccountUser.DoesNotExist:
            return HttpResponse("Wrong username or password")
        context = {username, password}
        return HttpResponse(context)
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
        password1 = str(pwd)
        account = AccountUser.objects.create(username=username,email=email,password=password1)
        account.save()
        return HttpResponse("Successfully!")
    return render(request, 'register.html', {})
