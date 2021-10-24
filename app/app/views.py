from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, "index.html", {})

def login_page(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            username = user.username
            return render(request, "index.html", {'username': username})
        else:
            messages.error(request,"Wrong")

    return render(request,"login.html", {})

def logout_page(request):
    logout(request)
    messages.success(request,"Logged Out Successfully!")
    return redirect('home')

def register_page(request):
    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST['email']
        password = request.POST['password']
        cofirmPassowrd = request.POST['cofirmpassword']

        myuser = User.objects.create_user(username, email, password)
        myuser.save()

        messages.success(request,"Your Account Successfully")

        return redirect('login')

    return render(request, "register.html")


def test_login(request):
    return render(request, "test-login.html")

def test_register(request):
    return render(request, "test-register.html")
