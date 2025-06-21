import django_filters
from django import forms
from project.NewsPortal.models import Post

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='По названию')
    author__user__username = django_filters.CharFilter(field_name='author__user__username', lookup_expr='icontains', label='По имени автора')
    created_at__gt = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gt',
        label='Позже указанной даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = []

