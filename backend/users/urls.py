from django.urls import path
from . import views

urlpatterns = [
    # path() для страницы регистрации нового пользователя
    # префикс auth/ обрабатывется в гл. urls.py
    path("signup/", views.SignUp.as_view(), name="signup")
]
