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
            username1 = serializer.data['username']
            password1 = serializer.data['password']
            email1 = serializer.data['email']
        # serializer = AccountSerializer(data=request.data)
        # if not serializer.is_valid():
            # username = serializer.data['username']
            # password = serializer.data['password']
        #     return Response('Wrong', status=status.HTTP_400_BAD_REQUEST)
            acc = Account.objects.create(username=username1, password=password1, email=email1)
            acc.save()
        # return redirect('loginView', foo="")
        return redirect('loginUser')
    return render(request, "registerView.html", {})


# def registerView(request):
#     return render(request, "registerView.html", {})