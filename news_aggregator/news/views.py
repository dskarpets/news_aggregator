from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from .models import NewsArticle, SavedArticle
from .services import NewsAPIService, CATEGORIES, SOURCES
from .translations import TranslationService, TRANSLATION_LANGUAGES


def index(request):
    """Main page with news articles"""
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin:index')
    category = request.GET.get('category', '')
    source = request.GET.get('source', '')
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)

    if search_query:
        articles = NewsAPIService.search_news(
            query=search_query,
            page=page
        )
    else:
        articles = NewsAPIService.fetch_top_headlines(
            category=category if category else None,
            source=source if source else None,
            page=page
        )

    saved_urls = []
    if request.user.is_authenticated:
        saved_urls = list(
            request.user.saved_articles.values_list('url', flat=True)
        )

    context = {
        'articles': articles,
        'saved_urls': saved_urls,
        'categories': CATEGORIES,
        'sources': SOURCES,
        'selected_category': category,
        'selected_source': source,
        'search_query': search_query,
        'current_page': int(page),
    }

    return render(request, 'news/index.html', context)


def article_detail(request, article_url):
    """News article detail page"""
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin:index')

    article = None
    try:
        article = NewsArticle.objects.get(url=article_url)
        article_data = {
            'title': article.title,
            'description': article.description,
            'content': article.content,
            'url': article.url,
            'image_url': article.image_url,
            'source': article.source,
        }
    except NewsArticle.DoesNotExist:
        article_data = request.session.get('current_article')
        if not article_data:
            messages.error(request, _('Article not found.'))
            return redirect('news:index')

    translate_to = request.GET.get('translate')
    if translate_to:
        article_data = TranslationService.translate_article(article_data, translate_to)

    is_saved = False
    if request.user.is_authenticated and article:
        is_saved = SavedArticle.objects.filter(
            user=request.user,
            article=article
        ).exists()

    context = {
        'article': article_data,
        'is_saved': is_saved,
        'translation_languages': TRANSLATION_LANGUAGES,
        'current_lang': translate_to or '',
    }

    return render(request, 'news/detail.html', context)


@login_required
def save_article(request):
    """Saving news article to read later list"""
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin:index')

    if request.method == 'POST':
        article_data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'content': request.POST.get('content'),
            'url': request.POST.get('url'),
            'image_url': request.POST.get('image_url'),
            'source': request.POST.get('source'),
        }

        article, created = NewsArticle.objects.get_or_create(
            url=article_data['url'],
            defaults=article_data
        )

        saved, created = SavedArticle.objects.get_or_create(
            user=request.user,
            article=article
        )

        if created:
            messages.success(request, _('Article added to reading list!'))
        else:
            messages.info(request, _('Article already in reading list.'))

        return redirect('news:index')

    return redirect('news:index')


@login_required
def remove_article(request, article_id):
    """Removing news article from list"""
    article = get_object_or_404(NewsArticle, id=article_id)
    SavedArticle.objects.filter(user=request.user, article=article).delete()
    messages.success(request, _('Article removed from reading list.'))
    return redirect('news:read_later')


@login_required
def read_later(request):
    """Read later list page"""
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin:index')

    saved_articles = SavedArticle.objects.filter(user=request.user).select_related('article')

    category = request.GET.get('category', '')
    source = request.GET.get('source', '')

    if category:
        saved_articles = saved_articles.filter(article__category=category)
    if source:
        saved_articles = saved_articles.filter(article__source=source)

    paginator = Paginator(saved_articles, 20)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    context = {
        'saved_articles': page_obj,
        'categories': CATEGORIES,
        'sources': SOURCES,
        'selected_category': category,
        'selected_source': source,
    }

    return render(request, 'news/read_later.html', context)


def store_article_in_session(request):
    if request.method == 'POST':
        article_data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'content': request.POST.get('content'),
            'url': request.POST.get('url'),
            'image_url': request.POST.get('image_url'),
            'source': request.POST.get('source'),
        }
        request.session['current_article'] = article_data
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
