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
from django.shortcuts import redirect
import pytz
from django.utils import timezone


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
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
        request.session['django_timezone'] = request.POST['timezone']
        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый пост
            form.save()
        return super().get(request, *args, **kwargs)


class AuthorDetailView(DetailView):
    template_name = 'authors_app/author_detail.html'
    queryset = Author.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(request.path)


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'authors_app/author_update.html'
    form_class = AuthorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(request.path)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Author.objects.get(pk=id)


class AuthorCreateView(CreateView):
    template_name = 'authors_app/author_create.html'
    form_class = AuthorForm
    success_url = '/sign/upgrade_to_author/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(request.path)

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
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(request.path)


