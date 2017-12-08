from rest_framework import serializers

from .models import Zipcode


class ZipcodeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'zipcode', 'query_count')
        model = Zipcode
