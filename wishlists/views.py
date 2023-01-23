from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions, status
from .models import Wishlist
from rooms.models import Room
from .serializers import WishlistSerializer


class Wishlists(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            all_wishlists, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user=request.user)
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        return Response(serializer.errors)


class WishlistDetail(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Wishlist.objects.get(pk=pk, user=self.request.user)
        except Wishlist.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    def delete(self, request, pk):
        wishlist = self.get_object(pk)
        wishlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        wishlist = self.get_object(pk)
        serializer = WishlistSerializer(wishlist, data=request.data, partial=True)
        if serializer.is_valid():
            updated_wishlist = serializer.save()
            serializer = WishlistSerializer(updated_wishlist)
            return Response(serializer.data)
        return Response(serializer.errors)


class WishlistToggle(APIView):
    def get_list(self, pk):
        try:
            return Wishlist.objects.get(pk=pk, user=self.request.user)
        except Wishlist.DoesNotExist:
            raise exceptions.NotFound

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk)
        room = self.get_room(room_pk)
        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=status.HTTP_200_OK)
