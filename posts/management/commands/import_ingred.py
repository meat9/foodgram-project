from django.core.management.base import BaseCommand
from django.contrib.auth.decorators import user_passes_test
import json
from posts.models import Ingredients, Tag


class Command(BaseCommand):
    help = "The Zen of Python"

    def handle(self, *args, **options):
        # @user_passes_test(lambda u: u.is_superuser)
        # def ingredients(request):

        with open("ingredients.json", "r", encoding="utf-8") as fh:
            data = json.load(fh)

        for i in data:
            dimension = i["dimension"]
            title = i["title"]

            if not Ingredients.objects.filter(title=title).first():
                if dimension in [
                    "по вкусу",
                    "стакан",
                    "кусок",
                    "горсть",
                    "банка",
                    "тушка",
                    "пакет",
                ]:
                    dimension = "г"
                ingredient = Ingredients(title=title, dimension=dimension)
                ingredient.save()
        tag_breakfast = Tag(name="Завтрак", slug="breakfast", color="orange")
        tag_breakfast.save()
        tag_lunch = Tag(name="Обед", slug="lunch", color="green")
        tag_lunch.save()
        tag_dinner = Tag(name="Ужин", slug="dinner", color="purple")
        tag_dinner.save()
        return HttpResponse("Добавлены ингредиенты\n".join(str(data)))
