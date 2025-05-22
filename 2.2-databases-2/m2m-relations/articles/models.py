from django.db import models
from django.core.exceptions import ValidationError


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']  # Сортировка статей по дате публикации (сначала новые)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название раздела")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ['name']  # Сортировка разделов по имени


class Scope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes', verbose_name="Статья")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Раздел")
    is_main = models.BooleanField(default=False, verbose_name="Основной")

    class Meta:
        verbose_name = "Тематика статьи"
        verbose_name_plural = "Тематики статей"
        # уникальность пары статья - тег
        unique_together = ('article', 'tag')

    def clean(self):
        # Валидация, что main может быть только один для данной статьи
        if self.is_main:
            existing_main_scopes = Scope.objects.filter(article=self.article, is_main=True)
            if self.pk:
                existing_main_scopes = existing_main_scopes.exclude(pk=self.pk)  # исключаем текущую запись при редактировании
            if existing_main_scopes.exists():
                raise ValidationError("Только один раздел может быть основным")

    def save(self, *args, **kwargs):
        self.clean()  # вызываем метод валидации
        super().save(*args, **kwargs)
