from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group, created = Group.objects.get_or_create(name='common')
        instance.groups.add(common_group)

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='Добро пожаловать!',
            message='Спасибо за регистрацию на нашем новостном портале! Мы рады видеть вас.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
        )