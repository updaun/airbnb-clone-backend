from django.shortcuts import render
from django.http import HttpResponse
from .models import Room, Amenity
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import AmenitiySerializer


# def see_all_rooms(request):
#     rooms = Room.objects.all()
#     return render(
#         request,
#         "rooms/all_rooms.html",
#         {"rooms": rooms, "title": "Hello! this title comes from django!"},
#     )


# def see_one_room(request, room_id):
#     try:
#         room = Room.objects.get(id=room_id)
#         return render(request, "rooms/room_detail.html", {"room": room})
#     except Room.DoesNotExist:
#         return render(request, "rooms/room_detail.html", {"not_found": True})


class Amenities(APIView):

    # http://127.0.0.1:8000/api/v1/rooms/amenities/
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitiySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitiySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitiySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(id=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitiySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitiySerializer(amenity, data=request.data, partial=True)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitiySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
