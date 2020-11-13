from django import template
from posts.models import FollowUser, FollowRecipe, ShoppingList

register = template.Library()


@register.filter(name='is_follow')
def is_follow(author, user):
    return FollowUser.objects.filter(user=user, author=author).exists()


@register.filter(name='is_favorite')
def is_favorite(recipe, user):
    return FollowRecipe.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='is_shop')
def is_shop(recipe, user):
    if user.is_authenticated:
        return ShoppingList.objects.filter(user=user, recipe=recipe).exists()
    else:
        return ShoppingList.objects.first()


@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('filters')


@register.filter(name="get_filter_link")
def get_filter_link(request, tag):
    new_request = request.GET.copy()

    if tag.slug in request.GET.getlist("filters"):
        filters = new_request.getlist("filters")
        filters.remove(tag.slug)
        new_request.setlist("filters", filters)
    else:
        new_request.appendlist("filters", tag.slug)

    return new_request.urlencode()
