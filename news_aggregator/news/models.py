from django.db import models
from django.conf import settings


class NewsArticle(models.Model):
    """News article model. It only contains articles that have been saved by users."""
    title = models.CharField(max_length=500, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Опис')
    content = models.TextField(blank=True, verbose_name='Вміст')
    url = models.URLField(max_length=1000, unique=True, verbose_name='URL')
    image_url = models.URLField(max_length=1000, blank=True, null=True, verbose_name='URL зображення')
    source = models.CharField(max_length=200, blank=True, verbose_name='Джерело')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата додавання')

    saved_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='saved_articles',
        through='SavedArticle',
        verbose_name='Збережено користувачами'
    )

    class Meta:
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SavedArticle(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Користувач'
    )
    article = models.ForeignKey(
        NewsArticle,
        on_delete=models.CASCADE,
        verbose_name='Новина'
    )
    saved_at = models.DateTimeField(auto_now_add=True, verbose_name='Збережено')

    class Meta:
        verbose_name = 'Збережена новина'
        verbose_name_plural = 'Збережені новини'
        unique_together = ['user', 'article']
        ordering = ['-saved_at']

    def __str__(self):
        return f'{self.user.username} - {self.article.title[:50]}'
