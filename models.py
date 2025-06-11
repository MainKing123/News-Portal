from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_ratings = sum(post.rating * 3 for post in self.post_set.all())
        comment_ratings = sum(comment.rating for comment in Comment.objects.filter(user=self.user))
        author_comment_ratings = sum(comment.rating for post in self.post_set.all() for comment in post.comment_set.all())
        self.rating = post_ratings + comment_ratings + author_comment_ratings
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article_type = models.CharField(max_length=10, choices=[('article', 'Статья'), ('news', 'Новость')])
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
