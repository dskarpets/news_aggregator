from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import NewsArticle, SavedArticle

User = get_user_model()


class NewsViewsTestCase(TestCase):

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.article = NewsArticle.objects.create(
            title='Test Article',
            description='Test description',
            content='Test content',
            url='https://example.com/test',
            source='Test Source'
        )

    def test_index_view_loads(self):
        """Main page loading test"""
        response = self.client.get(reverse('news:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/index.html')

    def test_index_view_with_authenticated_user(self):
        """Main page loading with authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('news:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('saved_urls' in response.context)

    def test_article_detail_view(self):
        """News article detail test"""
        session = self.client.session
        session['current_article'] = {
            'title': self.article.title,
            'description': self.article.description,
            'content': self.article.content,
            'url': self.article.url,
            'source': self.article.source,
        }
        session.save()

        response = self.client.get(
            reverse('news:article_detail', kwargs={'article_url': self.article.url})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/detail.html')

    def test_save_article_requires_login(self):
        """Saving article by unauthenticated user test"""
        response = self.client.post(reverse('news:save_article'), {
            'title': 'Test',
            'url': 'https://example.com/test2',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/users/login/' in response.url)

    def test_save_article_authenticated(self):
        """Saving article by authenticated user test"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(reverse('news:save_article'), {
            'title': 'New Article',
            'description': 'Description',
            'content': 'Content',
            'url': 'https://example.com/new',
            'source': 'Source',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            NewsArticle.objects.filter(url='https://example.com/new').exists()
        )

    def test_read_later_requires_login(self):
        """Access read later list by unauthenticated user test"""
        response = self.client.get(reverse('news:read_later'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/users/login/' in response.url)

    def test_read_later_authenticated(self):
        """Access read later list by authenticated user test"""
        self.client.login(username='testuser', password='testpass123')

        SavedArticle.objects.create(user=self.user, article=self.article)

        response = self.client.get(reverse('news:read_later'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/read_later.html')
        self.assertTrue('saved_articles' in response.context)

    def test_remove_article_from_list(self):
        """Removing article from list test"""
        self.client.login(username='testuser', password='testpass123')

        saved = SavedArticle.objects.create(user=self.user, article=self.article)

        response = self.client.get(
            reverse('news:remove_article', kwargs={'article_id': self.article.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            SavedArticle.objects.filter(user=self.user, article=self.article).exists()
        )

    def test_search_functionality(self):
        """Search functionality test"""
        response = self.client.get(reverse('news:index'), {'search': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['search_query'], 'test')

    def test_category_filter(self):
        """Category filtering test"""
        response = self.client.get(reverse('news:index'), {'category': 'technology'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_category'], 'technology')

    def test_source_filter(self):
        """Source filtering test"""
        response = self.client.get(reverse('news:index'), {'source': 'bbc-news'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_source'], 'bbc-news')


class NewsModelsTestCase(TestCase):

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.article = NewsArticle.objects.create(
            title='Test Article',
            description='Test description',
            content='Test content',
            url='https://example.com/test',
            source='Test Source',
        )

    def test_article_creation(self):
        """Article creation test"""
        self.assertEqual(self.article.title, 'Test Article')
        self.assertEqual(self.article.url, 'https://example.com/test')
        self.assertTrue(isinstance(self.article, NewsArticle))
        self.assertEqual(str(self.article), 'Test Article')

    def test_saved_article_creation(self):
        """Saved article creation test"""
        saved = SavedArticle.objects.create(
            user=self.user,
            article=self.article
        )
        self.assertEqual(saved.user, self.user)
        self.assertEqual(saved.article, self.article)
        self.assertTrue(isinstance(saved, SavedArticle))

    def test_saved_article_unique_constraint(self):
        """User can only save article once"""
        SavedArticle.objects.create(user=self.user, article=self.article)

        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            SavedArticle.objects.create(user=self.user, article=self.article)

    def test_article_url_unique(self):
        """Article unique constraint test"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            NewsArticle.objects.create(
                title='Another Article',
                url='https://example.com/test',
                source='Another Source'
            )

    def test_many_to_many_relationship(self):
        """Many-to-many relationship test"""
        SavedArticle.objects.create(user=self.user, article=self.article)

        self.assertEqual(self.article.saved_by.count(), 1)
        self.assertEqual(self.user.saved_articles.count(), 1)
        self.assertIn(self.article, self.user.saved_articles.all())
