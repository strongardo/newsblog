from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(verbose_name='Название', max_length=100)
    slug = models.SlugField(verbose_name='Слаг', max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse(
            'articles:category_detail',
            kwargs={
                'slug': self.slug,
            }
        )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(verbose_name='Слаг', max_length=200, unique=True)
    content = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)
    is_published = models.BooleanField(verbose_name='Опубликовано', default=False, db_index=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.PROTECT,
        related_name='articles'
    )
    image = models.ImageField(
        verbose_name='Фото',
        upload_to='articles/',
        blank=True
    )

    def get_absolute_url(self):
        return reverse(
            'articles:article_detail',
            kwargs={
                'slug': self.slug,
            }
        )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at', '-id']

    def __str__(self):
        return self.title


class Comment(models.Model):
    author_name = models.CharField(verbose_name='Автор', max_length=100)
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, db_index=True)
    article = models.ForeignKey(
        Article,
        verbose_name='Статья',
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f'Комментарий от {self.author_name} к {self.article}'
