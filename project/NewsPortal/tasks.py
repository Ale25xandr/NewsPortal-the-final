from datetime import datetime, timedelta

from celery import shared_task
from celery.beat import logger

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Category, Post


@shared_task
def week_post():
    d_1 = datetime(year=datetime.now().year,
                   month=datetime.now().month,
                   day=datetime.now().day,
                   hour=0,
                   minute=0,
                   second=0)
    d_2 = d_1 - timedelta(days=7)
    d = {}
    for i in range(1, len(Category.objects.all())):
        d[f"{Category.objects.get(id=i)}"] = Post.objects.filter(
            category=Category.objects.get(id=i), date_of_creation__range=[d_2, d_1])
        print(d)
    for k, v in d.items():
        e = Category.objects.get(category=f'{k}').subscrubers.all().values('email')
        print(e)
        email = [e[i]['email'] for i in range(0, len(e))]
        mail = EmailMultiAlternatives(
            subject=f'Все публикации за неделю в категории {k}',
            body='',
            from_email='Foma26199622@mail.ru',
            to=email
        )

        html = render_to_string('send_week.html',
                                context={'post': d[k],
                                         })

        mail.attach_alternative(html, 'text/html')

        mail.send()

        logger.info("Отправлено")


