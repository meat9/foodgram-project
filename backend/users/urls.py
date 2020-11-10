from django.urls import path
from . import views
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path() для страницы регистрации нового пользователя
    # префикс auth/ обрабатывется в гл. urls.py
    path("signup/", views.SignUp.as_view(), name="signup"),
    # path('password/change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('password/reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(),  name='password_reset_done'),
    # path('password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    # path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
    #path("password_change/", views.change_password, name='password_change_form'),
    #path("password-change/done", 'django.contrib.auth.views.password_change_done', name='password_change_done'),

