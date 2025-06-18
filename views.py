from django.shortcuts import render, get_object_or_404
from .models import Post

def news_list(request):
    news = Post.objects.order_by('-created_at')
    return render(request, 'news_list.html', {'news': news})

def news_detail(request, news_id):
    news_item = get_object_or_404(Post, pk=news_id)
    return render(request, 'news_detail.html', {'news_item': news_item})
