from django.shortcuts import render, redirect
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
            AccountUser.objects.filter(username=username).get(password=pwd)
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
        account = AccountUser.objects.create(username=username,email=email,password=pwd)
        account.save()
        return HttpResponse("Successfully!")
    return render(request, 'register.html', {})

def test_view(request):
    context = {}
    return render(request, 'base_index.html', context)