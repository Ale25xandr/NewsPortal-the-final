from django.template.loader import render_to_string

from .models import User, PostCategory
from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives


@receiver(m2m_changed, sender=PostCategory)
def notify(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        p = PostCategory.objects.filter(post_id=instance.id)
        d = {}
        for i in p:
            d[f'{i.category}'] = i.category.subscrubers.all().values('email')
        for k, v in d.items():
            email = [v[i]['email'] for i in range(0, len(v))]
            print(email)
            mail = EmailMultiAlternatives(
                subject=instance.heading,
                body='',
                from_email='Foma26199622@mail.ru',
                to=email
            )

            html = render_to_string('send.html',
                                    context={'post': instance,
                                             'category': k})

            mail.attach_alternative(html, 'text/html')

            mail.send()


@receiver(pre_save, sender=User)
def notify(sender, instance, **kwargs):
    if not User.objects.filter(username=instance.username):
        send_mail(
            subject=f'Вы успешно зарегистрировались!',
            message=f'{instance.username}, поздравляем! Теперь Вы зарегистрированный пользователь NewsPortal!',
            from_email='Foma26199622@mail.ru',
            recipient_list=[instance.email]
        )
    else:
        pass
