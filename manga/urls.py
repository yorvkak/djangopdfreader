from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('manga/<int:manga_id>/', views.manga_detail, name='manga_detail'),  # Страница манги
    path('chapter/<int:chapter_id>/', views.chapter_detail, name='chapter_detail'),  # Страница главы
    path('manga/<int:manga_id>/pdf/', views.generate_manga_pdf, name='generate_manga_pdf'),
    path('search/', views.search_manga, name='search_manga'),
    path('chapter/<int:chapter_id>/pdf/', views.view_pdf, name='view_pdf'),
    path('catalog/', views.manga_catalog, name='manga_catalog'),
]
