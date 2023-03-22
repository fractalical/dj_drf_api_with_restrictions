from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, FavouriteAdv
from advertisements.permissions import IsOwnerOrReadOnly, IsOwner, IsOwnerView
from advertisements.serializers import AdvertisementSerializer, \
    FavouriteAdvSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.filter(status__in=["OPEN", "CLOSED",
                                                        "Открыто", "Закрыто"])
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        print(self.action)
        if self.action in ["create", "update", "partial_update", "destroy"]:
            if self.action in ["update", "partial_update"]:
                self.queryset = Advertisement.objects.filter(
                    status__in=["OPEN", "CLOSED", "Открыто",
                                "Закрыто", "DRAFT", "Черновик"]
                )
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        elif self.action == "list":
            return [IsOwnerView()]
        return []

    @action(detail=False)
    def favourites_adv(self, request):

        if request.user.is_anonymous:
            msg = {"message":"You are not authenticated."}
            return Response(msg)
        user = request.user.id
        queryset = Advertisement.objects.filter(add_to_favourite=user)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsOwner]
    )
    def add_to_favourite(self, request, pk=None):

        adv = Advertisement.objects.get(id=int(pk))
        user = request.user
        if user.is_anonymous:
            msg = {"message":"You are not authenticated."}
        elif adv.status in ('DRAFT', 'Черновик'):
            msg = {"message":"Incorrect title id."}
        elif adv.creator_id == user.id:
            msg = {"message":"You are cannot add your own advertisement."}
        elif FavouriteAdv.objects.filter(user=user, advertisement=adv).exists():
            msg = {"message":"This ADV already added."}
        else:
            fav_adv = FavouriteAdv.objects.create(user=user, advertisement=adv)
            serializer = FavouriteAdvSerializer(fav_adv)
            return Response(serializer.data)
        return Response(msg)
