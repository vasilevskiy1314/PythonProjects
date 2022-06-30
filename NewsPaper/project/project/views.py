from rest_framework import viewsets
from rest_framework import permissions
from django.shortcuts import render
from news.serializers import *
from news.models import *
import django_filters


class PostViewset(viewsets.ModelViewSet):
   queryset = Post.objects.all()
   serializer_class = PostSerializer


class CategoryViewset(viewsets.ModelViewSet):
   queryset = Category.objects.all()
   serializer_class = CategorySerializer
   filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
   filterset_fields = ["name", "author_id"]


class AuthorViewset(viewsets.ModelViewSet):
   queryset = Author.objects.all()
   serializer_class = AuthorSerializer