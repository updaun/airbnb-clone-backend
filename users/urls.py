from django.urls import path
from .views import *

urlpatterns = [
    path("", Users.as_view()),
    path("me", Me.as_view()),
    path("change-password", ChangePassword.as_view()),
    path("@<str:username>", PublicUser.as_view()),
]
