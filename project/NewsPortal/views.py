import pytz
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, User, Author, Category
from datetime import datetime
from .filters import PostFilter
from .forms import PostFormCreate_and_Update, UserFormUpdate, UserPasswordChange
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.decorators import permission_required


class PostList(ListView):
    model = Post
    ordering = '-date_of_creation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        tzname = self.request.session["django_timezone"]
        tz = pytz.timezone(tzname)
        context['current_time'] = datetime.now(tz=tz)
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('post_list')


class PostListSearch(ListView):
    model = Post
    ordering = '-date_of_creation'
    template_name = 'post_search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now_time'] = datetime.now()
        context['filterset'] = self.filterset
        context['category'] = self.request.GET.get('category')
        context['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        return context

    def get_object(self, *args, **kwargs):
        obj = cache.get(self.kwargs['pk'], None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(self.kwargs['pk'], obj)
        return obj


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post',)
    form_class = PostFormCreate_and_Update
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        u = self.request.user
        a = Author.objects.get(user=u)
        form.instance.author = a
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post',)
    form_class = PostFormCreate_and_Update
    model = Post
    template_name = 'post_update.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsPortal.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class UserUpdate(UpdateView):
    form_class = UserFormUpdate
    model = User
    template_name = 'UserUpdate.html'
    success_url = reverse_lazy('post_list')


def logout_user(request):
    logout(request)
    return redirect('post_list')


def add_author(request):
    user = request.user
    authors_group = Group.objects.get(name='Authors')
    common_group = Group.objects.get(name='Common')
    if not request.user.groups.filter(name='Authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=request.user)
        common_group.user_set.remove(user)
    return redirect('post_list')


class User_password_change(PasswordChangeView):
    form_class = UserPasswordChange
    template_name = 'user_password_change.html'
    success_url = reverse_lazy('post_list')


class CategoryList(ListView):
    model = Post
    ordering = '-date_of_creation'
    template_name = 'category_list.html'
    context_object_name = 'cat_list'
    paginate_by = 4

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['is_not_subscribed'] = self.request.user not in self.category.subscrubers.all()
        context['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
        return context


def add_category(request, pk):
    user = request.user
    c = Category.objects.get(id=pk)
    c.subscrubers.add(user)

    send_mail(
        subject=f'Вы успешно подписались на рассылку в категории {c.category}!',
        message=f'{user.username}, поздравляем! Теперь Вы будете в курсе каждой новости, добавленной в '
                f'категорию {c.category}!',
        from_email='Foma26199622@mail.ru',
        recipient_list=[user.email]
    )
    return redirect('category_list', pk=pk)


class Ok_Email(TemplateView):
    template_name = 'ok_email.html'


@permission_required('NewsPortal.add_post', raise_exception=True)
def no_create(request):
    d_1 = datetime(year=datetime.now().year,
                   month=datetime.now().month,
                   day=datetime.now().day,
                   hour=0,
                   minute=0,
                   second=0)
    d_2 = datetime(year=datetime.now().year,
                   month=datetime.now().month,
                   day=datetime.now().day,
                   hour=23,
                   minute=59,
                   second=59)

    u = request.user
    a = Author.objects.get(user=u)
    p = Post.objects.filter(author=a, date_of_creation__range=[d_1, d_2])
    if len(p) >= 3:
        return redirect('create_no')
    else:
        return redirect('create')


class CreateNo(TemplateView):
    template_name = 'create_no.html'
