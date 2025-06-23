from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

@shared_task
def send_post_notification_email(subject, message, recipient_email):
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])

@shared_task
def send_weekly_digest_email(subject, recipient_email, html_content):
    msg = EmailMultiAlternatives(subject, 'Дайджест', settings.DEFAULT_FROM_EMAIL, [recipient_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task
def weekly_digest_task():
    from NewsPortal.models import Category
    from django.utils import timezone
    from datetime import timedelta

    now = timezone.now()
    last_week = now - timedelta(days=7)

    for category in Category.objects.all():
        posts = category.post_set.filter(date__gte=last_week)
        if not posts.exists():
            continue
        for user in category.subscribers.all():
            html_content = render_to_string('email/weekly_digest.html', {
                'posts': posts,
                'category': category,
                'user': user
            })
            send_weekly_digest_email.delay(
                f'Еженедельный дайджест: {category.name}', user.email, html_content
            )
