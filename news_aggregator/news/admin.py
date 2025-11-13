import requests
from django.shortcuts import render
from django.contrib import admin
from .models import NewsArticle, SavedArticle
from django.conf import settings


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'source','created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description', 'source']
    readonly_fields = ['created_at']


@admin.register(SavedArticle)
class SavedArticleAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'saved_at']
    list_filter = ['saved_at']
    search_fields = ['user__username', 'article__title']
    readonly_fields = ['saved_at']


class CustomAdminSite(admin.AdminSite):
    site_header = "Система агрегації новин"
    site_title = "Адмін-панель"
    index_title = "Моніторинг зовнішніх API"

    def each_context(self, request):
        context = super().each_context(request)

        apis = [
            {
                "name": "NewsAPI",
                "url": "https://newsapi.org/v2/top-headlines",
            },
            {
                "name": "Google Translate API",
                "url": "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=uk&dt=t&q=hello",
            },
        ]

        for api in apis:
            try:
                response = requests.get(
                    url=api["url"],
                    params={
                        "country": "us",
                        "apiKey": settings.NEWS_API_KEY
                    },
                    timeout=5
                )
                if response.status_code == 200:
                    api["status"] = f"🟢 Доступний | {response.status_code}"
                else:
                    api["status"] = f"🟠 Помилка {response.status_code}"
            except requests.exceptions.RequestException:
                api["status"] = f"🔴 Недоступний | {response.status_code}"

        context["external_apis"] = apis
        return context

    def index(self, request, extra_context=None):
        context = self.each_context(request)
        return render(request, "admin/custom_index.html", context)


custom_admin_site = CustomAdminSite(name="custom_admin")
custom_admin_site.register(NewsArticle, NewsArticleAdmin)
custom_admin_site.register(SavedArticle, SavedArticleAdmin)
