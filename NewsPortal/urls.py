"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from .NewsPortal import views

urlpatterns = [
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('news/search/', views.news_search, name='news_search'),

    path('news/create/', views.NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', views.NewsUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', views.NewsDelete.as_view(), name='news_delete'),

    path('articles/create/', views.ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', views.ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', views.ArticleDelete.as_view(), name='article_delete'),
    path('author/request/', views.author_request, name='author_request'),
]
