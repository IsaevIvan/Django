from django.http import HttpResponse
from django.shortcuts import render, reverse
import os, datetime

def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%H:%M:%S')
    formatted_date = current_time.strftime('%d.%m.%y')
    msg = f'Текущее время: {formatted_time}, <br>Текущая дата: {formatted_date}'
    return HttpResponse(msg)


def workdir_view(request):
    files_and_dirs = os.listdir()
    msg = 'Текущий список папок и файлов:<br>'
    for item in files_and_dirs:
        msg += f'- {item}<br>'
    return HttpResponse(msg)