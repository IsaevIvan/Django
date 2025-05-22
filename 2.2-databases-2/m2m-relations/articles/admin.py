from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope  # Импортируй все модели


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data and form.cleaned_data['is_main']:
                    count += 1
            except KeyError:
                pass  # форма удаляется, пропускаем

        if count == 0:
            raise ValidationError('Укажите основной раздел')
        if count > 1:
            raise ValidationError('Основным может быть только один раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope  # Используем модель Scope
    formset = ScopeInlineFormset  # Указываем класс FormSet для валидации
    extra = 1  # Добавляем одну пустую форму для добавления новых связей


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]  # Встраиваем ScopeInline в админку Article

# Необязательно, но рекомендуется для более удобного управления Tag
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass