from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    Recipe,
    Ingredients,
    Tag,
    RecipeIngredient,
    FollowUser,
    FollowRecipe,
    ShoppingList,
)


class MyUserAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + (
        "email",
        "first_name",
        "last_name",
        "username",
    )


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    list_filter = ("author", "title")
    inlines = (RecipeIngredientInline,)


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ("title", "dimension")
    list_filter = ("title",)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "amount")
    list_filter = ("ingredient",)


class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "author")
    fields = ("user", "author")


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    fields = ("user", "recipe")


class ShopListAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    fields = ("user", "recipe")


admin.site.register(Tag, TagAdmin)

admin.site.register(Recipe, RecipeAdmin)

admin.site.register(Ingredients, IngredientsAdmin)

admin.site.register(RecipeIngredient, RecipeIngredientAdmin)

admin.site.register(FollowUser, FollowAdmin)

admin.site.register(FollowRecipe, FavoritesAdmin)

admin.site.register(ShoppingList, ShopListAdmin)
