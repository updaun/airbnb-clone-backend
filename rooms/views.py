from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


def see_all_rooms(request):
    rooms = Room.objects.all()
    return render(
        request,
        "rooms/all_rooms.html",
        {"rooms": rooms, "title": "Hello! this title comes from django!"},
    )


def see_one_room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        return render(request, "rooms/room_detail.html", {"room": room})
    except Room.DoesNotExist:
        return render(request, "rooms/room_detail.html", {"not_found": True})
