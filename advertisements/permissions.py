from rest_framework.permissions import BasePermission

from advertisements.models import Advertisement


class IsOwnerView(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            if int(request.query_params.get('creator')) == request.user.id:
                view.queryset = Advertisement.objects.filter(
                    status__in=["OPEN", "CLOSED", "Открыто",
                                "Закрыто", "DRAFT", "Черновик"])
        return True


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
