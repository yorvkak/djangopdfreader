from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Genre, Author, Manga, Chapter

# Register your models here.

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')

@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'display_genres', 'display_cover', 'upload_date')
    list_filter = ('genres',)
    list_display_links = ('title',)
    search_fields = ('title', 'author__name')  # Add search functionality


    def display_genres(self, obj):
        return ', '.join(genre.name for genre in obj.genres.all())

    display_genres.short_description = 'Жанры'

    def display_cover(self, obj):
        return mark_safe(f'<img src="{obj.cover.url}" width="100" height="150" />')

    display_cover.short_description = 'Обложка'

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'manga', 'chapter_number', 'title', 'release_date')
    list_filter = ('manga',)
    list_display_links = ('manga',)
    search_fields = ('title',)  # Add search functionality

    def manga_title(self, obj):
        return obj.manga.title

    manga_title.short_description = 'Манга'

    def pdf_file_link(self, obj):
        return f'<a href="{obj.pdf_file.url}" target="_blank">Download PDF</a>'

    pdf_file_link.short_description = 'PDF File'

admin.site.site_header = 'Manga Admin'  # Customize the admin site header
