from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from baseApp.databases.models import Account
from baseApp.repositories.serializers import AccountSerializer


# @api_view(['POST'])
def loginUser(request):
    if request.method == "POST":
        serializer = AccountSerializer(data=request.POST)
        if serializer.is_valid():
            username_login = serializer.data['username']
            password_login = serializer.data['password']
            try:
                account = Account.objects.filter(username=username_login).get(password=password_login)
                
                return Response(account, status=status.HTTP_200_OK)
            except Account.DoesNotExist:
                return Response('Wrong', status=status.HTTP_400_BAD_REQUEST)
    # serializer = AccountSerializer(data=request.data)
    # if serializer.is_valid():
    #     username1 = serializer.data['username']
    #     password1 = serializer.data['password']
    #     try:
    #         username = Account.objects.filter(username=username1).get(password=password1)
    #     except Account.DoesNotExist:
    #         return Response('Wrong', status=status.HTTP_400_BAD_REQUEST)

    # return Response(data=serializer.data,status=status.HTTP_200_OK)
    return render(request, "loginView.html", {})