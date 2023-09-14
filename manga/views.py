from django.conf import settings
from django.core.paginator import Page
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.shortcuts import render
import os
from .models import Manga, Chapter  # Import your models
from django.http import JsonResponse
from django.http import FileResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import datetime



# Your other view functions go here

def all_latest_added_mangas(request):
    # Получите список недавно добавленной манги
    latest_added_mangas = Manga.objects.order_by('-upload_date')

    paginator = Paginator(latest_added_mangas, 12)
    page_number = request.GET.get('page_mangas')
    latest_mangas = paginator.get_page(page_number)

    context = {
        'latest_mangas': latest_mangas,
    }

    return render(request, 'all_latest_added_mangas.html', context)

def all_latest_mangas(request):
    current_date = datetime.now()

    # Получите список манг, у которых есть новые главы
    mangas_with_new_chapters = Manga.objects.filter(
        chapter__release_date__lte=current_date
    ).distinct().order_by('-id')

    # Получите последние главы для каждой манги
    for manga in mangas_with_new_chapters:
        latest_chapter = Chapter.objects.filter(manga=manga).order_by('-release_date').first()
        manga.latest_chapter = latest_chapter  # Добавляем атрибут latest_chapter к каждой манге

    paginator = Paginator(mangas_with_new_chapters, 12)
    page_number = request.GET.get('page_mangas')
    latest_mangas = paginator.get_page(page_number)
    context = {
        'latest_mangas': latest_mangas,
    }

    return render(request, 'all_latest_mangas.html', context)

def manga_catalog(request):
    mangas = Manga.objects.all()
    page = request.GET.get('page')  # Получаем номер текущей страницы из параметра GET-запроса
    paginator = Paginator(mangas, 12)  # Разбиваем список манг на страницы по 12 манг на каждой

    try:
        mangas = paginator.page(page)
    except PageNotAnInteger:
        # Если параметр page не является целым числом, отображаем первую страницу
        mangas = paginator.page(1)
    except EmptyPage:
        # Если параметр page больше, чем доступное количество страниц, отображаем последнюю страницу
        mangas = paginator.page(paginator.num_pages)

    return render(request, 'catalog.html', {'page': mangas})

def main(request):
    query = request.POST.get('q', '')  # Получаем запрос из строки поиска
    results = []

    if query:
        # Ищем мангу по названию, используя метод filter
        results = Manga.objects.filter(title__icontains=query)

    return render(request, 'index.html', {'results': results, 'query': query})

def search_manga(request):
    query = request.GET.get('q')  # Получаем запрос из строки поиска
    if query:
        # Ищем мангу по названию, используя метод filter
        results = Manga.objects.filter(title__icontains=query)
    else:
        results = []

    return render(request, 'search_results.html', {'results': results, 'query': query})


def index(request):
    # Получите список последних добавленных манг
    latest_mangas_list = Manga.objects.order_by('-id')[:24]
    paginator = Paginator(latest_mangas_list, 12)
    page_number = request.GET.get('page_mangas')  # Получите номер текущей страницы
    latest_mangas = paginator.get_page(page_number)

    # Получите список последних глав
    latest_chapters_list = Chapter.objects.order_by('-release_date')[:24]
    paginator_chapters = Paginator(latest_chapters_list, 12)
    page_number_chapters = request.GET.get('page_chapters')  # Получите номер текущей страницы для глав
    latest_chapters = paginator_chapters.get_page(page_number_chapters)

    context = {
        'latest_mangas': latest_mangas,
        'latest_chapters': latest_chapters,
    }

    return render(request, 'index.html', context)

def manga_detail(request, manga_id):
    manga = Manga.objects.get(pk=manga_id)
    if Chapter.objects.filter(manga=manga):
        latest_chapter = Chapter.objects.filter(manga=manga).latest('release_date')
    else:
        latest_chapter = None
    chapters = manga.chapter_set.all()
    context = {
        'manga': manga,
        'chapters': chapters,
        'latest_chapter': latest_chapter,  # Добавьте latest_chapter в контекст
    }
    return render(request, 'details.html', context)

def chapter_detail(request, chapter_id):
    chapter = Chapter.objects.get(pk=chapter_id)
    return render(request, 'details.html', {'chapter': chapter})

def view_pdf(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    pdf_file = chapter.pdf_file.path  # Предположим, что у вас есть поле pdf_file в модели Chapter, которое хранит путь к PDF-файлу.
    response = FileResponse(open(pdf_file, 'rb'), content_type='application/pdf')
    return response

def generate_manga_pdf(request, manga_id):
    manga = get_object_or_404(Manga, pk=manga_id)
    pages = Page.objects.filter(chapter__manga=manga).order_by('chapter__chapter_number', 'page_number')

    # Create a BytesIO buffer to receive the PDF data.
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)

    # Loop through the pages and add them to the PDF.
    for page in pages:
        # Get the image path for the page.
        image_path = os.path.join(settings.MEDIA_ROOT, str(page.image))

        # Calculate the width and height of the image to fit the PDF page.
        width, height = letter
        img_width, img_height = p.drawInlineImage(image_path, 0, 0, width, height)

        # Add a new page for the next image.
        p.showPage()

    # Save the PDF to the buffer.
    p.save()

    # Set the buffer's position to the beginning.
    buffer.seek(0)

    # Create a response with the PDF file.
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{manga.title}.pdf"'
    return response
