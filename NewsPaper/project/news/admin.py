from django.contrib import admin
from .models import Category, Author, Post, PostCategory, Comment
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)


nullfy_rating.short_description = 'Обнулить рейтинг'


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating', 'dateCreation')
    list_filter = ('title', 'author', 'dateCreation', 'postCategory__name')
    search_fields = ('title', 'author__authorUser__username', 'postCategory__name')
    actions = [nullfy_rating]


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)

