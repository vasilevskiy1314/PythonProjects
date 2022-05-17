from django_filters import FilterSet
from news.models import Author
from django import template

register = template.Library()


class AuthorFilter(FilterSet):
    class Meta:
        model = Author
        fields = {
            'ratingAuthor': ['gt'],
            'nameAuthor': ['icontains']
        }