import django_filters
from django_filters import FilterSet, DateTimeFilter
from .models import Post, Category
from django.forms import DateTimeInput
from django.utils.translation import gettext_lazy as _

cat_name_qc = Category.objects.all().values('category')
cat_name_qn = Category.objects.all().values('id')
cat_name_l = [(cat_name_qn[i]['id'], f"{(cat_name_qc[i]['category'])}") for i in range(0, len(cat_name_qc))]
print(cat_name_l)


class PostFilter(FilterSet):
    article = django_filters.ChoiceFilter(label=_('Type'), choices=Post.articl, empty_label=' ')
    heading = django_filters.CharFilter(label=_('Heading'), lookup_expr='icontains')
    category = django_filters.ChoiceFilter(label=_('Category'), choices=cat_name_l)
    added_after = DateTimeFilter(
        field_name='date_of_creation',
        lookup_expr='gt',
        label=_('Date of creation (no later than)'),
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'date'},
        ),
    )
