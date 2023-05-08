from .models import Category, Post
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category', )


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('heading', 'text', 'article', )

