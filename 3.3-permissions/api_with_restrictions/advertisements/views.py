from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from .models import Advertisement, Favorite, AdvertisementStatusChoices
from .serializers import AdvertisementSerializer
from .permissions import IsAdminOrOwner  # Нужно создать этот permission


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Для анонимных пользователей скрываем черновики
        if not self.request.user.is_authenticated:
            return queryset.exclude(status=AdvertisementStatusChoices.DRAFT)

        # Для обычных пользователей:
        if not self.request.user.is_staff:
            return queryset.exclude(
                # Скрываем чужие черновики
                models.Q(status=AdvertisementStatusChoices.DRAFT) &
                ~models.Q(creator=self.request.user)
            )

        # Админы видят все объявления
        return queryset

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdminOrOwner()]
        return []

    # Добавляем эндпоинт для избранного
    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        ad = self.get_object()
        if ad.creator == request.user:
            return Response(
                {"error": "Нельзя добавить своё объявление в избранное"},
                status=status.HTTP_400_BAD_REQUEST
            )

        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            advertisement=ad
        )

        if not created:
            return Response({"status": "Уже в избранном"})
        return Response({"status": "Добавлено в избранное"}, status=status.HTTP_201_CREATED)

    # Эндпоинт для списка избранного
    @action(detail=False)
    def favorites(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        ads = [fav.advertisement for fav in favorites]
        serializer = self.get_serializer(ads, many=True)
        return Response(serializer.data)