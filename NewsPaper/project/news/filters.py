from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Author
from django import template

register = template.Library()


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'rating': ['gt'],
            'dateCreation': ['gt'],
        }
