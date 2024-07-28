"""
Serialzers for the user app.
"""

from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['name',
                  'email',
                  'password',
                  'mobile',]
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }