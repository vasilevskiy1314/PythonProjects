from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from project import views


router = routers.DefaultRouter()
router.register(r'news', views.PostViewset)
router.register(r'categorys1', views.CategoryViewset)
router.register(r'authors1', views.AuthorViewset)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('protect.urls')),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
    path('authors/', include('authors.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('contacts/', include('django.contrib.flatpages.urls')),
    path('posts/', include('news.urls')),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
