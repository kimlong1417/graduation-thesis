from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from baseApp.api.serializers import RegisAccountSerializer

@api_view(['POST',])
def registration(request):
    if request.method == 'POST':
        serializer = RegisAccountSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "successfully save"
            data['username'] = account.username
        else:
            data = serializer.errors
        return Response(data)