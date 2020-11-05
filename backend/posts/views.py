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
    all_tags = Tag.objects.all()
    user = User.objects.get(username=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            form.instance.author = user
            form.save()
            form.errors
            return redirect('index')
        else:

            return HttpResponse(form.errors)
    else:
        form = PostForm(request.POST, files=request.FILES or None)
        return render(request, 'formRecipe.html', {'form': form, 'all_tags': all_tags})


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


def profile1(request, username):
    post_author = get_object_or_404(User, username=username)
    profile = Post.objects.filter(author = post_author).order_by("-pub_date").all()
    paginator = Paginator(profile, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    count = Post.objects.filter(author=post_author).count()
    if request.user.is_authenticated:
        follow_count = Follow.objects.filter(user=post_author).count()
        f_count = Follow.objects.filter(author=post_author).count()
        following = Follow.objects.filter(author=post_author, user=request.user).count()
        return render(request,'profile.html', {'post_author': post_author, 'paginator': paginator,'page': page, 'count': count, 
        'following' : following, 'follow_count' : follow_count, 'f_count' : f_count})
    else:
        return render(request,'profile.html', {'post_author': post_author, 'paginator': paginator,'page': page, 'count': count})
    
        
def post_view(request, username, post_id):
    post_author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author=post_author, pk=post_id)
    count = Post.objects.filter(author=post_author).count()
    com = Comment.objects.filter(post=post)
    form = CommentForm()
    return render(request, "singlePage.html", {'post_author': post_author, 'post': post,'count': count, "com" : com, "form" : form})

 
#@login_required
def post_edit(request, username, post_id):
    text_head = 'Изменить запись'
    text_button = 'Сохранить'
    post_author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id, author=post_author)
    if request.user == post_author:
        if request.method == 'POST':
            form = PostForm(request.POST or None, files=request.FILES or None, instance=post) 
            if form.is_valid():
                form.save()
                return redirect(post_view, username, post_id)  
            else:
  
                return redirect(post_edit, username, post_id)
        else:
            form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
            return render(request, 'new.html', {'form': form, 'post': post, 'text_head': text_head, 'text_button': text_button})
    else:
        return redirect(post_view, username, post_id)


def page_not_found(request, exception):
        return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
        return render(request, "misc/500.html", status=500)