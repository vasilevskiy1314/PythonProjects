from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, View
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .tasks import new_post_sub_email
from django.core.cache import cache
from datetime import datetime, timedelta
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils.translation import gettext as _


class CategorysList(ListView):
    model = Category
    template_name = 'news_app/categorys.html'
    context_object_name = 'categorys'
    ordering = ['name']
    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'news_app/category_detail.html'
    context_object_name = 'category'
    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        return context


@login_required
def add_subscribe(request, pk):
    sub_user = User.objects.get(id=request.user.pk)
    category_object = Category.objects.get(pk=pk)
    category_object.subscribers.add(sub_user)
    return redirect('/posts/categorys/')


@login_required
def del_subscribe(request, pk):
    sub_user = User.objects.get(id=request.user.pk)
    category_object = Category.objects.get(pk=pk)
    category_object.subscribers.remove(sub_user)
    return redirect('/posts/categorys/')


class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-dateCreation']
    paginate_by = 10  # поставим постраничный вывод в один элемент
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['value1'] = None
        context['form'] = PostForm()
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'news_app/post_search.html'
    context_object_name = 'posts'
    ordering = ['dateCreation']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()  # добавим переменную текущей даты time_now
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetailView(DetailView):
    template_name = 'news_app/post_detail.html'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_time_creation'] = self.object.dateCreation.strftime("%d-%B-%Y %H:%M")
        return context

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'Post-{self.kwargs["pk"]}',
                        None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'Post-{self.kwargs["pk"]}', obj)

        return obj


class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'news_app/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            sub_categoryname = Category(request.POST['postCategory'])
            new_post_sub_email.apply_async([sub_categoryname.pk], countdown=1)
        return redirect('/posts')


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'news_app/post_update.html'
    form_class = PostForm
    permission_required = ('news.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'news_app/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'
    permission_required = ('news.delete_post')