from django.contrib.auth.models import User
from rest_framework import serializers

#serializers to convert python datatypes to be converted to json/xml/etc and vice-versa

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        #make password only visible on user creation, not when retieving info about the user, otherwise password will be exposed
        extra_kwargs = {"password" : {"write_only": True}}
        
    def create(self, validatedData):
        #user will be created if user data/fields are validated by previous check
        user = User.objects.create_user(**validatedData)
        return user