from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
import csv


def index(request):
    return redirect(reverse('bus_stations'))

CSV_FILE_PATH = '/home/ivan/dj-homeworks/1.2-requests-templates/pagination/data-398-2018-08-30.csv'

def read_bus_stations(file_path):
    stations = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stations.append(row)  # Добавляем каждую строку в список
    return stations


def read_bus_stations(file_path):
    stations = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stations.append(row)  # Добавляем каждую строку в список
    return stations

def index(request):
    return redirect(reverse('bus_stations'))

def bus_stations(request):
    bus_stations_list = read_bus_stations(CSV_FILE_PATH)
    paginator = Paginator(bus_stations_list, 10)  # Показывать по 10 станций на странице

    page_number = request.GET.get('page', 1)  # Получаем номер страницы из GET-запроса или устанавливаем 1 по умолчанию
    page_obj = paginator.get_page(page_number)  # Получаем объекты для текущей страницы

    context = {
        'bus_stations': page_obj,
        'page': page_obj.number,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
    }

    return render(request, 'stations/index.html', context)
