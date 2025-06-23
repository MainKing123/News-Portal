from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from NewsPortal.tasks import send_post_notification_email
from django.conf import settings
from NewsPortal.models import Post

@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group, created = Group.objects.get_or_create(name='common')
        instance.groups.add(common_group)

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_post_notification_email.delay(
            'Добро пожаловать!',
            'Спасибо за регистрацию на нашем новостном портале! Мы рады видеть вас.',
            instance.email
        )


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        for category in instance.category.all():
            for user in category.subscribers.all():
                message = f"Новая статья: {instance.title}\n\n{instance.text[:100]}...\n\nЧитать: http://127.0.0.1:8000/news/{instance.pk}"
                send_post_notification_email.delay(
                    f"Новая статья в категории {category.name}",
                    message,
                    user.email
                )
