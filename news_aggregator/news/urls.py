from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
    path('article/<path:article_url>/', views.article_detail, name='article_detail'),
    path('save/', views.save_article, name='save_article'),
    path('remove/<int:article_id>/', views.remove_article, name='remove_article'),
    path('read-later/', views.read_later, name='read_later'),
    path('store-article/', views.store_article_in_session, name='store_article'),
]
