from rest_framework import serializers

from baseApp.databases.models import Account, Image


class RegisAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'password', 'email']


class AccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)

class ImageSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image_base64']

class ImageSerializer(serializers.Serializer):
    image_base64 = serializers.CharField(max_length=10000)