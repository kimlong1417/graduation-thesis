from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Account
from .forms import AccountForm

# Create your views here.

def home(request):
    accounts = Account.objects.all()
    context = {'accounts': accounts}
    return render(request,'home.html', context)

def register(request):
    form = AccountForm()
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form
    }
    return render(request,'register.html', context)