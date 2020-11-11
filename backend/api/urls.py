from django.urls import path
from . import views


urlpatterns = [
    path("ingredients/", views.Ingredient.as_view()),
    path("favorites/", views.Favorites.as_view()),
    path("favorites/<int:recipe_id>", views.Favorites.as_view()),
    path("subscriptions/", views.Subscribe.as_view()),
    path("subscriptions/<int:author_id>", views.Subscribe.as_view()),
    path("purchases/", views.Purchase.as_view()),
    path("purchases/<int:recipe_id>", views.Purchase.as_view()),
]
