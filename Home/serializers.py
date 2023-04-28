from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from Home.models import *

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = API_Device_data
        fields = '__all__'



class AuthCustomTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username, password=password
            )
            print("*" * 100)
            if not user:
                raise exceptions.AuthenticationFailed(
                    'Unable to log in with provided credentials'
                )
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
