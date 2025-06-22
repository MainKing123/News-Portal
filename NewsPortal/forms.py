from django import forms
from NewsPortal.models import Post
from .models import AuthorRequest

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']

        widgets = {
            'article_type': forms.HiddenInput(), # Скрываем поле article_type из формы
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Явное указание виджета для каждой категории
        self.fields['categories'].widget = forms.CheckboxSelectMultiple

class AuthorRequestForm(forms.ModelForm):
    class Meta:
        model = AuthorRequest
        fields = [] # Форма без полей, только подтверждение запроса