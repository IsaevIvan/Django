from django.contrib.auth.models import User
from rest_framework import serializers
from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at')
        read_only_fields = ('creator', 'created_at')

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        user = self.context['request'].user
        current_status = data.get('status')

        # Проверяем только если статус OPEN или не указан (по умолчанию OPEN)
        if current_status == AdvertisementStatusChoices.OPEN or current_status is None:
            # Получаем количество открытых объявлений пользователя
            open_ads = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN
            )

            # Если это обновление существующего объявления, исключаем его из подсчета
            if self.instance and self.instance in open_ads:
                open_ads = open_ads.exclude(id=self.instance.id)

            if open_ads.count() >= 10:
                raise serializers.ValidationError(
                    "У пользователя не может быть больше 10 открытых объявлений."
                )

        return data
