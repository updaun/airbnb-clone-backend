from rest_framework import serializers
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitiySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomDetailSerializer(serializers.ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitiySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "name",
            "country",
            "city",
            "price",
        )
