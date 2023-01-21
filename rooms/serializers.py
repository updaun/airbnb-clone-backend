from rest_framework import serializers
from .models import Amenity


class AmenitiySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"
