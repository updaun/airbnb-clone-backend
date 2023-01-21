from django.shortcuts import render
from django.http import HttpResponse
from .models import Room, Amenity
from rest_framework.views import APIView
from rest_framework.response import Response
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
    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
