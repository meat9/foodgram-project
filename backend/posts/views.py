import datetime as dt
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Recipe, Ingredients, FollowUser, ShoppingList, RecipeIngredient, Tag
from .utils import get_ingredients


def index(request):
    tags_filter = request.GET.getlist('filters')
    recipe_list = Recipe.objects.order_by('-pub_date').all()
    all_tags = Tag.objects.all()
    if tags_filter:
        recipe_list = recipe_list.filter(
            tags__slug__in=tags_filter).distinct().all()
    paginator = Paginator(recipe_list, 6) # показывать по 10 записей на странице.
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number) # получить записи с нужным смещением
    return render(request, 'indexAuth.html', {'page': page, 'paginator': paginator, 'all_tags': all_tags})

def new_post(request):
    user = User.objects.get(username=request.user)
    all_tags = Tag.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')
        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = user
            recipe.save()
            for ing_name, amount in ingredients.items():
                ingredient = get_object_or_404(Ingredients, title=ing_name)
                recipe_ing = RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=amount
                )
                recipe_ing.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'formRecipe.html', {'form': form,'all_tags': all_tags})

def recipe_view(request, recipe_id, username):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    username = get_object_or_404(User, username=username)
    return render(request, 'singlePage.html', {'username': username, 'recipe': recipe, })

def profile(request, username):
    username = get_object_or_404(User, username=username)
    
    tag = request.GET.getlist('filters')
    #recipes = Recipe.objects.filter(author=username).select_related('author').all()
    recipes = Recipe.objects.filter(author=username).order_by("-pub_date").all()
    all_tags = Tag.objects.all()
    if tag:
        recipes = recipes.filter(tags__slug__in=tag)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    # if request.user.is_authenticated:
    #     following = FollowUser.objects.filter(user=request.user).\
    #         filter(author=username).select_related('author')
    #     if not following:
    #         following = None
    #     else:
    #         following = True
    #     return render(request, "authorRecipe.html",{'username': username, 'page': page,'paginator': paginator, 'following': following})
    return render(request, "authorRecipe.html",{'username': username, 'page': page,'paginator': paginator,'all_tags':all_tags })

def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    all_tags = Tag.objects.all()
    if request.user != recipe.author:
        return redirect('index')
    if request.method == "POST":
        form = PostForm(request.POST or None, files=request.FILES or None, instance=recipe)
        ingredients = get_ingredients(request)
        if form.is_valid():
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for item in ingredients:
                RecipeIngredient.objects.create(
                    #units=ingredients[item],
                    ingredient=Ingredients.objects.get(title=f'{item}'),
                    recipe=recipe,)
                    #amount=amount)
            form.save_m2m()
        return redirect('index')
    form = PostForm(request.POST or None, files=request.FILES or None, instance=recipe)
    return render(request, 'recipe_edit.html', {'form': form, 'recipe': recipe, 'all_tags': all_tags})


def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
    return redirect('index')












def page_not_found(request, exception):
        return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
        return render(request, "misc/500.html", status=500)