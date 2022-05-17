from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('categorys/', CategorysList.as_view(), name='categorys'),
    path('categorys/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('categorys/<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
    path('categorys/<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),
]