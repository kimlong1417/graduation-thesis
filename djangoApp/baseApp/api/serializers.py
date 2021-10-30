from rest_framework import serializers

from baseApp.models import Account

class RegisAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'password']