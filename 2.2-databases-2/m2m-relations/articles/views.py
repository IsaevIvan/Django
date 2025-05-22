
from django.shortcuts import render
from .models import Article

def articles_list(request):
    template = 'articles/news.html'

    # Получаем статьи из базы данных и упорядочиваем их
    articles = Article.objects.all().order_by('-published_at')

    # Создаем контекст и передаем статьи в шаблон под именем 'object_list'
    context = {'object_list': articles}

    return render(request, template, context)