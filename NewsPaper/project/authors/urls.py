from django.urls import path
from .views import AuthorsList, AuthorDetailView, AuthorUpdateView, AuthorCreateView, AuthorSearch


urlpatterns = [
    path('', AuthorsList.as_view()),
    path('<int:pk>', AuthorDetailView.as_view(), name='author_detail'),
    path('<int:pk>/edit/', AuthorUpdateView.as_view(), name='author_update'),
    path('add/', AuthorCreateView.as_view(), name='author_create'),
    path('search/', AuthorSearch.as_view(), name='author_search'),

]