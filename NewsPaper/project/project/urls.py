from django.contrib import admin
from django.urls import path, include

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
]
