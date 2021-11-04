from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Account
from baseApp.api.serializers import AccountSerializer

# Create your views here.
# class AccountAPIView(APIView):
@api_view(['POST'])
def registerUser(request):
    serializer = AccountSerializer(data=request.data)
    if not serializer.is_valid(): 
        return Response('Wrong', status=status.HTTP_400_BAD_REQUEST)
    username = serializer.data['username']
    passoword = serializer.data['password']
    acc = Account.objects.create(username=username,password=passoword)
    return Response(data=acc.username, status=status.HTTP_200_OK)

@api_view(['POST'])
def loginUser(request):
    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid():
        username1 = serializer.data['username']
        password1 = serializer.data['password']
        try:
            username = Account.objects.filter(username=username1).get(password=password1)
        except Account.DoesNotExist:
            return Response('Wrong', status=status.HTTP_400_BAD_REQUEST)

    return Response(data=serializer.data,status=status.HTTP_200_OK)