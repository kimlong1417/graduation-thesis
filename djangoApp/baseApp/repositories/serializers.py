from rest_framework import serializers

from baseApp.databases.models import Account, Images

class RegisAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'password', 'email']
        

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['image_id', 'images']
        
class ImgSerializer(serializers.Serializer):
    images = serializers.CharField(max_length = 1000)
    

class AccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
    
    