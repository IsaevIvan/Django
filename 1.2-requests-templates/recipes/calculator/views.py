from django.http import HttpResponse
from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    'salat' : {
        'яйца, шт': 1,
        'помидор, шт': 1,
        'сыр, ломтик': 1,
        'огурец, шт' : 1,
    }
    # можете добавить свои рецепты ;)
}

def home_view(request):
    recipe_names = DATA.keys()
    return render(request, 'calculator/home.html', {'recipe_names': recipe_names})



def recipe_view(request, dish):

    if dish in DATA:
        recipe = DATA[dish]
        context = {'recipe': recipe}
        return render(request, 'calculator/index.html', context)
    else:
        return HttpResponse(f"Рецепт для '{dish}' не найден.")  # Или можно использовать 404.