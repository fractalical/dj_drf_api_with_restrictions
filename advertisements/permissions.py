from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        elif request.user.is_staff:
            return True
        return request.user == obj.creator


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user != obj.creator
