import requests
from django.conf import settings
import re


class NewsAPIService:
    """NewsAPI Service designed to provide news articles from different sources"""
    BASE_URL = 'https://newsapi.org/v2'

    @classmethod
    def fetch_top_headlines(cls, category=None, source=None, page=1, page_size=20):
        """Отримання головних новин"""
        url = f'{cls.BASE_URL}/top-headlines'
        params = {
            'apiKey': settings.NEWS_API_KEY,
            'page': page,
            'pageSize': page_size,
        }

        if source:
            params['sources'] = source
        else:
            params['country'] = 'us'
            if category:
                params['category'] = category

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return cls._process_articles(data.get('articles', []))
            return []
        except Exception as e:
            print(f'Error fetching news: {e}')
            return []

    @classmethod
    def search_news(cls, query, page=1, page_size=20):
        """Search news articles"""
        url = f'{cls.BASE_URL}/everything'
        params = {
            'apiKey': settings.NEWS_API_KEY,
            'q': query,
            'page': page,
            'pageSize': page_size,
            'sortBy': 'relevancy',
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return cls._process_articles(data.get('articles', []))
            return []
        except Exception as e:
            print(f'Error searching news: {e}')
            return []

    @classmethod
    def _clean_content(cls, content):
        """Method designed for cleaning news content by removing invalid characters"""
        if not content:
            return ''

        if '[+' in content and 'chars]' in content:
            content = content.split('[+')[0].strip()

        if 'PROMOTED' in content:

            before_promoted = content.split('PROMOTED')[0].strip()

            if len(before_promoted) > 50:
                content = before_promoted
            else:
                return ''

        copyright_markers = [
            'E-mail :',
            '[email protected]',
            '+380 95 641 22 07',
            'R40-02280',
            'R40-02162',
            '01032,',
            '© 2014-2025',
        ]

        for marker in copyright_markers:
            if marker in content:
                before_marker = content.split(marker)[0].strip()
                if len(before_marker) > 50:
                    content = before_marker
                else:
                    return ''

        content = re.sub(r'^[\(\)\s\-\r\n]+', '', content)

        if len(content) < 100:
            return ''

        words = [w for w in content.split() if len(w) > 0]
        if not words:
            return ''

        short_words = [w for w in words if len(w) <= 2]
        if len(short_words) > len(words) * 0.6:
            return ''

        return content.strip()

    @classmethod
    def _process_articles(cls, articles):
        """Process articles"""
        processed = []
        for article in articles:
            if not article.get('title') or article.get('title') == '[Removed]':
                continue

            content = cls._clean_content(article.get('content', ''))

            description = article.get('description', '')
            if not content and not description:
                continue

            processed_article = {
                'title': article.get('title', ''),
                'description': description,
                'content': content,
                'url': article.get('url', ''),
                'image_url': article.get('urlToImage', ''),
                'source': article.get('source', {}).get('name', ''),
            }
            processed.append(processed_article)

        return processed


CATEGORIES = [
    ('general', 'General'),
    ('business', 'Business'),
    ('technology', 'Technology'),
    ('entertainment', 'Entertainment'),
    ('health', 'Health'),
    ('science', 'Science'),
    ('sports', 'Sports'),
]

SOURCES = [
    ('bbc-news', 'BBC News'),
    ('cnn', 'CNN'),
    ('reuters', 'Reuters'),
    ('al-jazeera-english', 'Al Jazeera'),
    ('the-verge', 'The Verge'),
    ('techcrunch', 'TechCrunch'),
    ('espn', 'ESPN'),
]
