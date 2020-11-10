from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new_post, name="new_post"),
    path("favorite/", views.favorite, name="favorite"),
    path("follow/", views.follow, name="follow"),
    path("shopping-list/", views.shopping_list, name='shopping_list'),
    path('download_card', views.download_card, name='download_card'),
    path("<username>/", views.profile, name="profile"),
    path("<username>/<int:recipe_id>/", views.recipe_view, name="recipe_view"),
    path('recipe/<int:recipe_id>/edit', views.recipe_edit, name='recipe_edit'),
    path('recipe/<int:recipe_id>/delete', views.recipe_delete, name='recipe_delete'),



]
