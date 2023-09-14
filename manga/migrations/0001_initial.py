# Generated by Django 4.2.4 on 2023-09-03 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Жанр')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Manga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('cover', models.ImageField(upload_to='mangas/', verbose_name='Обложка')),
                ('upload_date', models.DateField(verbose_name='Дата выпуска')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manga.author')),
                ('genres', models.ManyToManyField(to='manga.genre', verbose_name='Жанры')),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('chapter_number', models.PositiveIntegerField(verbose_name='Номер главы')),
                ('release_date', models.DateField(verbose_name='Дата выпуска')),
                ('pdf_file', models.FileField(upload_to='pdfs/', verbose_name='PDF файл')),
                ('manga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manga.manga')),
            ],
            options={
                'verbose_name': 'Глава',
                'verbose_name_plural': 'Главы',
                'unique_together': {('manga', 'chapter_number')},
            },
        ),
    ]
