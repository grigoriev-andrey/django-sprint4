from doctest import debug_script

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.db import models
from django.utils import timezone

from .constants import FIELD_MAX_LENGTH

User = get_user_model()


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        'Опубликовано', default=True, blank=False,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        'Добавлено', auto_now_add=True, blank=False
    )

    class Meta:
        abstract = True


class Category(PublishedModel):
    title = models.CharField(
        'Заголовок', max_length=FIELD_MAX_LENGTH, blank=False
    )
    description = models.TextField('Описание', blank=False)
    slug = models.SlugField(
        'Идентификатор', max_length=FIELD_MAX_LENGTH, blank=False, unique=True,
        help_text='Идентификатор страницы для URL; разрешены символы '
                  'латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        ordering = ('-title',)
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(
        'Название места', max_length=FIELD_MAX_LENGTH, blank=False
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedModel):
    title = models.CharField(
        'Заголовок', max_length=FIELD_MAX_LENGTH, blank=False
    )
    text = models.TextField('Текст', blank=False)
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        blank=True,
        null=True,
        default=timezone.now,
        help_text='Если установить дату и время в будущем — можно делать '
                  'отложенные публикации.'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='posts',
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=False, null=True,
        related_name='posts',
        verbose_name='Категория'

    )
    image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )

    @property
    def comment_count(self):
        return self.comments.count()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Comment(PublishedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    text = models.TextField(
        'Текст комментария',
        max_length=FIELD_MAX_LENGTH,
        help_text='Введите текст комментария (до 256 символов)'
    )
    created_at = models.DateTimeField(
        'Дата и время комментария', auto_now_add=True
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text



