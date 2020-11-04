from .models import ShoppingList, Tag, Post


def counter(request):
    if request.user.is_authenticated:
        count = ShoppingList.objects.filter(user=request.user).count()
    else:
        count = None
    return {'count': count}


def all_tags(request):
    """Вывод всех тегов."""

    all_tags = Tag.objects.all()
    #all_tags = Post.objects.all()
    return {'all_tags': all_tags}


def url_parse(request):
    """Установка фильтров в урл страницы."""

    result_str = ''
    for item in request.GET.getlist('filters'):
        result_str += f'&filters={item}'
    return {'filters': result_str}
