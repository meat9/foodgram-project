from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static


handler404 = "posts.views.page_not_found"  # noqa
handler500 = "posts.views.server_error"  # noqa

urlpatterns = [
    # раздел администратора
    path("admin/", admin.site.urls),
    # flatpages
    path("about/", include("django.contrib.flatpages.urls")),
    # регистрация и авторизация
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    # импорт из приложения posts
    path("api/v1/", include("api.urls")),
    path("", include("posts.urls")),
]

urlpatterns += [
    path("about-us/", views.flatpage, {"url": "/about-us/"}, name="about"),
    path("terms/", views.flatpage, {"url": "/terms/"}, name="terms"),
    path(
        "about-author/", views.flatpage, {"url": "/about-author/"}, name="about-author"
    ),
    path("about-spec/", views.flatpage, {"url": "/about-spec/"}, name="about-spec"),
]
