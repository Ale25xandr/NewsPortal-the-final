from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from .models import Post


class PostFormCreate_and_Update(forms.ModelForm):
    class Meta:
        model = Post
        labels = {
                  'article': _('Type'),
                  'category': _('Category'),
                  'heading': _('Heading'),
                  'text': _('Text'),
                  }
        fields = ['article', 'category', 'heading', 'text']
        localized_fields = ['article', 'category', 'heading', 'text']


class UserFormUpdate(forms.ModelForm):
    class Meta:
        model = User
        labels = {'username': _('Username'),
                  'first_name': _('First name'),
                  'last_name': _('Last name'),
                  'email': _('E-mail')}
        fields = ['first_name', 'last_name', 'email', 'username']
        localized_fields = fields
        help_texts = {'username': ' '}


class UserPasswordChange(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label='Повторите новый пароль',
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        g = Group.objects.get(name='Common')
        g.user_set.add(user)
        return user
