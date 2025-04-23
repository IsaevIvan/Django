from django.shortcuts import render, redirect, get_object_or_404

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort_param = request.GET.get('sort')
    phones = Phone.objects.all()  # Получаем все объекты Phone

    if sort_param == 'name':
        phones = phones.order_by('name')
    elif sort_param == 'min_price':
        phones = phones.order_by('price')
    elif sort_param == 'max_price':
        phones = phones.order_by('-price')
    # else:  # Если sort_param не указан, оставляем phones в исходном порядке (или по умолчанию, если есть)

    template = 'catalog.html'
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):

    phone = get_object_or_404(Phone, slug=slug)
    template = 'product.html'
    context = {'phone': phone}
    return render(request, template, context)