from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, AuthorRequest
from django.contrib.auth.models import Group

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(AuthorRequest)

@admin.register(AuthorRequest)
class AuthorRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'request_date', 'approved')

    def save_model(self, request, obj, form, change):
        if obj.approved and not change: # Если запрос одобрен и это новое создание
            authors_group, created = Group.objects.get_or_create(name='authors')
            obj.user.groups.add(authors_group)
            Author.objects.create(user=obj.user)

        super().save_model(request, obj, form, change)
