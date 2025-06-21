from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from project.NewsPortal.models import Post
from project.NewsPortal.forms import PostForm
from project.NewsPortal.filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


@login_required # доступ только авторизованным пользователям
def news_list(request):
    news_list = Post.objects.filter(article_type='news').order_by('-created_at')
    paginator = Paginator(news_list, 10)
    page = request.GET.get('page')

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    return render(request, 'news_list.html', {'news': news})


@login_required # доступ только авторизованным пользователям
def news_detail(request, news_id):
    news_item = get_object_or_404(Post, pk=news_id)
    return render(request, 'news_detail.html', {'news_item': news_item})


@login_required # доступ только авторизованным пользователям
def news_search(request):
    news = Post.objects.filter(article_type='news').order_by('-created_at')
    post_filter = PostFilter(request.GET, queryset=news)
    news = post_filter.qs

    return render(request, 'news_search.html', {'filter': post_filter, 'news': news})


class NewsCreate(LoginRequiredMixin, CreateView): # доступ только авторизованным пользователям
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_type = 'news'
        post.author = self.request.user.author
        return super().form_valid(form)


class ArticleCreate(LoginRequiredMixin, CreateView): # доступ только авторизованным пользователям
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_type = 'article'
        post.author = self.request.user.author
        return super().form_valid(form)
class NewsUpdate(LoginRequiredMixin, UpdateView): # доступ только авторизованным пользователям
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')

    def get_object(self, queryset=None): # проверка прав доступа
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user.author:
            raise PermissionDenied
        return obj


class ArticleUpdate(LoginRequiredMixin, UpdateView): # доступ только авторизованным пользователям
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')

    def get_object(self, queryset=None): # проверка прав доступа
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user.author:
            raise PermissionDenied
        return obj


class NewsDelete(LoginRequiredMixin, DeleteView): # доступ только авторизованным пользователям
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')

    def get_object(self, queryset=None): # проверка прав доступа
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user.author:
            raise PermissionDenied
        return obj


class ArticleDelete(LoginRequiredMixin, DeleteView): # доступ только авторизованным пользователям
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')

    def get_object(self, queryset=None): # проверка прав доступа
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user.author:
            raise PermissionDenied
        return obj
