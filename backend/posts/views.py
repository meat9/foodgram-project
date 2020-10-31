import datetime as dt
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .models import Post, User, Follow, Ingredient


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10) # показывать по 10 записей на странице.
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number) # получить записи с нужным смещением
    #return render(request, 'index.html', {'page': page, 'paginator': paginator})
    return render(request, 'indexAuth.html', {'page': page, 'paginator': paginator})


@login_required
def new_post(request):
    text_head = 'Добавить запись'
    text_button = 'Добавить'
    if request.method == "POST":
        form = PostForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            name = form.cleaned_data["name"]
            image = form.cleaned_data["image"]
            text = form.cleaned_data["text"]
            ingredient = form.cleaned_data["ingredient"]
            tag = form.cleaned_data["tag"]
            time_to_made = form.cleaned_data["time_to_made"]
            # text = form.cleaned_data["text"]
            # group = form.cleaned_data["group"]
            # image = form.cleaned_data["image"]
            Post.objects.create(
                author=request.user, 
                name=name,
                image=image, 
                text=text, 
                ingredient=ingredient, 
                tag=tag, 
                time_to_made=time_to_made)
            return redirect('index')
        else:
            return render(request, 'new.html', {'form': form, 'text_head': text_head, 'text_button': text_button})
    else:
        form = PostForm(request.POST, files=request.FILES or None)
        return render(request, 'new.html', {'form': form, 'text_head': text_head, 'text_button': text_button})


def profile(request, username):
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
    return render(request, "post.html", {'post_author': post_author, 'post': post,'count': count, "com" : com, "form" : form})


@login_required
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