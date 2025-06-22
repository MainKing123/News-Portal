from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsPortal.models import Post, Category

class Command(BaseCommand):
    help = 'Отправка еженедельной рассылки с новыми статьями'

    def handle(self, *args, **kwargs):
        one_week_ago = timezone.now() - timedelta(days=7)
        categories = Category.objects.all()

        for category in categories:
            posts = category.post_set.filter(date__gte=one_week_ago)
            if not posts.exists():
                continue

            subscribers = category.subscribers.all()
            if not subscribers:
                continue

            for user in subscribers:
                html_content = render_to_string(
                    'email/weekly_digest.html',
                    {'posts': posts, 'category': category, 'user': user}
                )

                msg = EmailMultiAlternatives(
                    subject=f'Новые статьи в категории "{category.name}" за неделю',
                    body='Тексты статей во вложении.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()