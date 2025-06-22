from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")

    def update_rating(self):
        # Рейтинг постов автора
        post_ratings = Post.objects.filter(author=self).aggregate(total_rating=Sum('rating'))['total_rating'] or 0
        post_ratings *= 3

        # Рейтинг комментариев, оставленных автором
        comment_ratings = Comment.objects.filter(user=self.user).aggregate(total_rating=Sum('rating'))['total_rating'] or 0

        # Рейтинг комментариев к постам автора
        author_comment_ratings = Comment.objects.filter(post__author=self).aggregate(total_rating=Sum('rating'))['total_rating'] or 0

        self.rating = post_ratings + comment_ratings + author_comment_ratings
        self.save()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    article_type = models.CharField(
        max_length=10,
        choices=[('article', 'Статья'), ('news', 'Новость')],
        verbose_name="Тип статьи",
        help_text="Выберите тип публикации: статья или новость."
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    categories = models.ManyToManyField(Category, through='PostCategory', verbose_name="Категории")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")

    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"Комментарий от {self.user.username} к {self.post.title}"

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]

@receiver(post_save, sender=Comment)
def update_author_rating_on_comment(sender, instance, **kwargs):
    instance.post.author.update_rating()

@receiver(post_save, sender=Post)
def update_author_rating_on_post(sender, instance, **kwargs):
    instance.author.update_rating()


class AuthorRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Запрос на авторство от {self.user.username}"