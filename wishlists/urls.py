from django.urls import path
from .views import *

urlpatterns = [
    path("", Wishlists.as_view()),
]
