from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions, status
from .models import Photo
from django.conf import settings
import requests


class PhotoDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise exceptions.NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        # if photo.room:
        #     if photo.room.owner != request.user:
        #         raise exceptions.PermissionDenied
        # elif photo.experience:
        #     if photo.experience.host != request.user:
        #         raise exceptions.PermissionDenied
        if (photo.room and photo.room.owner != request.user) or (
            photo.experience and photo.experience.host != request.user
        ):
            raise exceptions.PermissionDenied
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetUploadURL(APIView):
    def post(self, request):
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload"
        one_time_url = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {settings.CF_TOKEN}",
            },
        )
        one_time_url = one_time_url.json()
        return Response(one_time_url)
