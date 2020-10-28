from django.contrib import admin
from .models import Post, Ingredient

class PostAdmin(admin.ModelAdmin):
    # поля, отображаемые в админке
    list_display = ('pk', 'name', 'image', 'text', 'ingredient', 'tag', 'time_to_made')
    # поиск по тексту постов
    search_fields = ('text',)
    # фильтрация по дате
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'  # где пусто - там будет эта строка (для всех колонок)

admin.site.register(Post, PostAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'quantity', 'dimension')
    search_fields = ('text',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
