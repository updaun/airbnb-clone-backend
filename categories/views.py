from django.http import JsonResponse
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import Category
from .serializers import CategorySerializer

# restframework 없이 api를 만드는 방법
# def categories(request):
#     all_categories = Category.objects.all()
#     return JsonResponse(
#         {
#             "ok":True,
#             "categories":serializers.serialize("json", all_categories),
#         }
#     )


@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)


@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)
