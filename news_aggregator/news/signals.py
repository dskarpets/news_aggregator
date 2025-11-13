from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import SavedArticle


@receiver(post_delete, sender=SavedArticle)
def delete_orphaned_article(sender, instance, **kwargs):
    """Deletes news article that are not saved by any user"""
    article = instance.article

    if not SavedArticle.objects.filter(article=article).exists():
        article.delete()
