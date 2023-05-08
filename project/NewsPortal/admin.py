from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Post, Category


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post


admin.site.register(Post)
admin.site.register(Category)
