from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from news.models import NewsArticle, SavedArticle

User = get_user_model()


class NewsAppEndToEndTest(TestCase):
    """End-to-end test"""

    def setUp(self):
        self.client = Client()
        self.article = NewsArticle.objects.create(
            title='Test Article',
            description='Description',
            content='Content',
            url='https://example.com/test',
            source='Source',
        )

    def test_full_user_flow(self):
        """
        Scenario:
        1. User registration
        2. User log in
        3. Main page loading
        4. News article detail loading
        5. Saving article to "Read later"
        6. Check if article is present is the list
        7. Deleting from list
        8. User log out
        """

        register_response = self.client.post(reverse('users:register'), {
            'username': 'e2e_user',
            'email': 'e2e@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertEqual(register_response.status_code, 302)
        self.assertTrue(User.objects.filter(username='e2e_user').exists())

        login_response = self.client.post(reverse('users:login'), {
            'username': 'e2e_user',
            'password': 'TestPass123!',
        })
        self.assertEqual(login_response.status_code, 302)

        index_response = self.client.get(reverse('news:index'))
        self.assertEqual(index_response.status_code, 200)

        self.assertEqual(index_response.status_code, 200)
        self.assertTemplateUsed(index_response, 'news/index.html')

        session = self.client.session
        session['current_article'] = {
            'title': self.article.title,
            'description': self.article.description,
            'content': self.article.content,
            'url': self.article.url,
            'source': self.article.source,
        }
        session.save()

        detail_response = self.client.get(reverse('news:article_detail', kwargs={'article_url': self.article.url}))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, 'Test Article')

        save_response = self.client.post(reverse('news:save_article'), {
            'title': self.article.title,
            'description': self.article.description,
            'content': self.article.content,
            'url': self.article.url,
            'source': self.article.source,
        })
        self.assertEqual(save_response.status_code, 302)
        self.assertTrue(SavedArticle.objects.filter(article=self.article).exists())

        read_later_response = self.client.get(reverse('news:read_later'))
        self.assertEqual(read_later_response.status_code, 200)
        self.assertContains(read_later_response, 'Test Article')

        remove_response = self.client.get(reverse('news:remove_article', kwargs={'article_id': self.article.id}))
        self.assertEqual(remove_response.status_code, 302)
        self.assertFalse(SavedArticle.objects.filter(article=self.article).exists())

        logout_response = self.client.get(reverse('users:logout'))
        self.assertEqual(logout_response.status_code, 302)
        after_logout = self.client.get(reverse('news:index'))
        self.assertFalse(after_logout.wsgi_request.user.is_authenticated)
