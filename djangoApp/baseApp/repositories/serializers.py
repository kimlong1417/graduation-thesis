from rest_framework import serializers

from baseApp.databases.models import Account

class RegisAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'password', 'email']

class AccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
    