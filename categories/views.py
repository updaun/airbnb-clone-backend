from django.http import JsonResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import render
from .models import Category
from .serializers import CategorySerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


# restframework 없이 api를 만드는 방법
# def categories(request):
#     all_categories = Category.objects.all()
#     return JsonResponse(
#         {
#             "ok":True,
#             "categories":serializers.serialize("json", all_categories),
#         }
#     )


# @api_view(["GET", "POST"])
# def categories(request):
#     if request.method == "GET":
#         all_categories = Category.objects.all()
#         serializer = CategorySerializer(all_categories, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             new_category = serializer.save()
#             return Response(CategorySerializer(new_category).data)
#         else:
#             return Response(serializer.errors, status=400)


# @api_view(["GET", "PUT", "DELETE"])
# def category(request, pk):
#     try:
#         category = Category.objects.get(pk=pk)
#     except Category.DoesNotExist:
#         raise NotFound

#     if request.method == "GET":
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = CategorySerializer(category, data=request.data, partial=True)
#         if serializer.is_valid():
#             updated_category = serializer.save()
#             return Response(CategorySerializer(updated_category).data)
#         else:
#             return Response(serializer.data)
#     elif request.method == "DELETE":
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class Categories(APIView):
#     def get(self, request):
#         all_categories = Category.objects.all()
#         serializer = CategorySerializer(all_categories, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             new_category = serializer.save()
#             return Response(CategorySerializer(new_category).data)
#         else:
#             return Response(serializer.errors, status=400)


# class CategoryDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Category.objects.get(pk=pk)
#         except Category.DoesNotExist:
#             raise NotFound

#     def get(self, request, pk):
#         serializer = CategorySerializer(self.get_object(pk))
#         return Response(serializer.data)

#     def put(self, request, pk):
#         serializer = CategorySerializer(
#             self.get_object(pk), data=request.data, partial=True
#         )
#         if serializer.is_valid():
#             updated_category = serializer.save()
#             return Response(CategorySerializer(updated_category).data)
#         else:
#             return Response(serializer.data)

#     def delete(self, request, pk):
#         self.get_object(pk).delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
