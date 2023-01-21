from rest_framework import serializers
from .models import Amenity, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        depth = 1


class AmenitiySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"
