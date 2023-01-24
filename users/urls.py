from django.urls import path
from .views import Me

urlpatterns = [path("me", Me.as_view())]
