from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from news.models import Author
from datetime import datetime
from .filters import AuthorFilter
from .forms import AuthorForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class AuthorsList(ListView):
    model = Author
    template_name = 'authors.html'
    context_object_name = 'authors'
    ordering = ['-ratingAuthor']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        context['filter'] = AuthorFilter(self.request.GET, queryset=self.get_queryset())
        context['value1'] = None
        context['form'] = AuthorForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый пост
            form.save()
        return super().get(request, *args, **kwargs)


class AuthorDetailView(DetailView):
    template_name = 'authors_app/author_detail.html'
    queryset = Author.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'authors_app/author_update.html'
    form_class = AuthorForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Author.objects.get(pk=id)


class AuthorCreateView(CreateView):
    template_name = 'authors_app/author_create.html'
    form_class = AuthorForm
    success_url = '/sign/upgrade_to_author/'


class AuthorSearch(ListView):
    model = Author
    template_name = 'authors_app/author_search.html'
    context_object_name = 'authors'
    ordering = ['-ratingAuthor']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        context['filter'] = AuthorFilter(self.request.GET, queryset=self.get_queryset())
        return context


