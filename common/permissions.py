from strawberry.types import Info
import typing
from strawberry.permission import BasePermission


class OnlyLoggedIn(BasePermission):
    message = "You need to be logged in for this!"

    def has_permission(self, source: typing.Any, info: Info):
        return info.context.user.is_authenticated
