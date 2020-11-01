from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    quantity = models.FloatField(max_length=20)
    dimension = models.TextField()
    #     slug = models.SlugField(unique=True)
    #     description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.ingredient


class Post(models.Model):
    CHOICES = (
        ('Завтрак', 'Завтрак'),
        ('Обед', 'Обед'),
        ('Ужин', 'Ужин'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_posts")
    name = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    text = models.TextField()
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="ingredient", blank=True, null=True)
    tag = models.CharField(max_length=300, choices=CHOICES)
    time_to_made = models.IntegerField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    def __str__(self):
       return self.text


# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_comments")
#     text = models.TextField()
#     created  = models.DateTimeField("date published", auto_now_add=True)
#     def __str__(self):
#        return self.text


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
