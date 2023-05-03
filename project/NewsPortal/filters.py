import django_filters
from django_filters import FilterSet, DateTimeFilter
from .models import Post, Category
from django.forms import DateTimeInput

cat_name_qc = Category.objects.all().values('category')
cat_name_qn = Category.objects.all().values('id')
cat_name_l = [(cat_name_qn[i]['id'], f"{cat_name_qc[i]['category']}") for i in range(0, len(cat_name_qc))]


class PostFilter(FilterSet):
    article = django_filters.ChoiceFilter(label='Тип', choices=Post.articl, empty_label=' ')
    heading = django_filters.CharFilter(label='Заголовок', lookup_expr='icontains')
    category = django_filters.ChoiceFilter(label='Категория', choices=cat_name_l)
    added_after = DateTimeFilter(
        field_name='date_of_creation',
        lookup_expr='gt',
        label='Дата создания (не позднее)',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'date'},
        ),
    )
