from django.db import models


class Genre(models.Model):
    name = models.CharField("Жанр", max_length=100)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

class Author(models.Model):
    name = models.CharField(max_length=100)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

class Manga(models.Model):
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    cover = models.ImageField("Обложка", upload_to="mangas/")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Assuming ForeignKey to Author
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    upload_date = models.DateField("Дата выпуска")

    def __str__(self):
        return self.title


class Chapter(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    title = models.CharField("Заголовок", max_length=100)
    chapter_number = models.PositiveIntegerField("Номер главы")
    release_date = models.DateField("Дата выпуска")
    pdf_file = models.FileField("PDF файл", upload_to="pdfs/")  # Only allow PDF files

    def __str__(self):
        return f"{self.manga.title} - Глава {self.chapter_number}: {self.title}"

    class Meta:
        verbose_name = "Глава"
        verbose_name_plural = "Главы"
        unique_together = ("manga", "chapter_number")
