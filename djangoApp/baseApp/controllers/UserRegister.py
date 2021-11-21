from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from baseApp.databases.models import Account
from baseApp.repositories.serializers import AccountSerializer




# @api_view(['POST'])
def registerUser(request):
    if request.method == "POST":
        serializer = AccountSerializer(data=request.POST)
        if serializer.is_valid():
            username_register = serializer.data['username']
            password_register = serializer.data['password']
            email_register = serializer.data['email']
        # serializer = AccountSerializer(data=request.data)
        # if not serializer.is_valid(): 
            # username = serializer.data['username']
            # password = serializer.data['password']
            # return Response('Wrong', status=status.HTTP_400_BAD_REQUEST)
            acc = Account.objects.create(username=username_register, password=password_register, email=email_register)
            acc.save()
        # return redirect('loginView', foo="")
        # return redirect('loginUser')
        return Response(serializer.data)
    return render(request, "registerView.html", {})


# def registerView(request):
#     return render(request, "registerView.html", {})