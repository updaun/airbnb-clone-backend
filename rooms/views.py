from django.db import transaction
from django.conf import settings
from django.utils import timezone
from .models import Room, Amenity
from categories.models import Category
from bookings.models import Booking
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from .serializers import *
from reviews.serializers import ReviewSerializer
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer
from medias.serializers import PhotoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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
            return Response(serializer.errors, status=400)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(id=pk)
        except Amenity.DoesNotExist:
            raise exceptions.NotFound

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
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Rooms(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise exceptions.ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise exceptions.ParseError("The category kind should be rooms.")
            except Category.DoesNotExist:
                raise exceptions.ParseError("Category not found")
            try:
                with transaction.atomic():
                    room = serializer.save(owner=request.user, category=category)
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                    serializer = RoomDetailSerializer(
                        room, context={"request": request}
                    )
                    return Response(serializer.data)
            except Exception:
                raise exceptions.ParseError("Amenity not found")
        else:
            return Response(serializer.errors, status=400)


class RoomDetail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return Room.objects.get(id=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise exceptions.PermissionDenied
        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise exceptions.ParseError("The category kind should be rooms.")
            except Category.DoesNotExist:
                raise exceptions.ParseError("Category not found")
            try:
                with transaction.atomic():
                    if category_pk:
                        room = serializer.save(category=category)
                    else:
                        room = serializer.save()

                    amenities = request.data.get("amenities")
                    if amenities:
                        room.amenities.clear()
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                    serializer = RoomDetailSerializer(room)
                return Response(serializer.data)
            except Exception:
                raise exceptions.ParseError("Amenity not found")
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise exceptions.PermissionDenied
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return Room.objects.get(id=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = ReviewSerializer(room.reviews.all()[start:end], many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=request.user, room=self.get_object(pk))
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(id=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        serializer = AmenitiySerializer(room.amenities.all()[start:end], many=True)
        return Response(serializer.data)


class RoomPhotos(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise exceptions.PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


class RoomBookings(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,
        )
        # bookings = Booking.objects.filter(room__pk=pk)
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(
            data=request.data,
            context={"room": room},
        )
        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class RoomBookingCheck(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        check_out = request.query_params.get("check_out")
        check_in = request.query_params.get("check_in")
        exists = Booking.objects.filter(
            room=room,
            check_in__lte=check_out,
            check_out__gte=check_in,
        ).exists()
        if exists:
            return Response({"ok": False})
        return Response({"ok": True})


def make_error(request):
    division_by_zero = 1 / 0
