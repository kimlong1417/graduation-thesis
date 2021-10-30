from rest_framework import serializers
from .models import member

class MemberSerializers(serializers.ModelSerializer):
    class Meta():
        model = member
        fields = ('firstname','lastname', 'username', 'password', 'email', 'phone')