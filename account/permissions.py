from rest_framework import permissions
from friendship.models import *
from .models import *


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj, account):
        if request.user:
            return account == request.user
        return False


class IsAccountOwnerOrIsFriend(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user2 = User.objects.get(username=obj)
        if request.user.is_superuser:
            return True
        print(Friend.objects.are_friends(user1=request.user, user2=user2))
        return Friend.objects.are_friends(user1=request.user, user2=user2) is True or request.user == user2


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user


class IsAdminOrAccountOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        try:
            obj = obj.user
        except AttributeError:
            print('Catching Attribute Error in permissions check')
            obj = obj

        return obj.id == request.user.id or request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser
