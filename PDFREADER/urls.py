"""
URL configuration for PDFREADER project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from manga import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Главная страница
    path('manga/<int:manga_id>/', views.manga_detail, name='manga_detail'),  # Страница манги
    path('manga/<int:manga_id>/pdf/', views.generate_manga_pdf, name='generate_manga_pdf'),
    path('chapter/<int:chapter_id>/', views.chapter_detail, name='chapter_detail'),
    path('search/', views.search_manga, name='search_manga'),
    path('chapter/<int:chapter_id>/pdf/', views.view_pdf, name='view_pdf'),
    path('catalog/', views.manga_catalog, name='manga_catalog'),
    path('all_latest_mangas/', views.all_latest_mangas, name='all_latest_mangas'),
    path('all_latest_added_mangas/', views.all_latest_added_mangas, name='all_latest_added_mangas'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)