from django import forms
from project.NewsPortal.models import Post

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
