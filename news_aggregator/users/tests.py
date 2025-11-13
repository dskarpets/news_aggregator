from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewsTestCase(TestCase):

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_register_view_get(self):
        """Registration page loading test"""
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertContains(response, 'Sign Up')

    def test_register_view_post_valid(self):
        """Valid data registration test"""
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_post_invalid(self):
        """Invalid data registration test"""
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': 'pass',
            'password2': 'different',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_login_view_get(self):
        """Login page loading test"""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_post_valid(self):
        """Valid data login test"""
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_post_invalid(self):
        """Invalid data login test"""
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_view(self):
        """Log out test"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:logout'))

        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('news:index'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_profile_view_requires_login(self):
        """Unauthorized access to user profile test"""
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/users/login/' in response.url)

    def test_profile_view_authenticated(self):
        """Authorized access to user profile test"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, 'testuser')

    def test_profile_update(self):
        """Profile update test"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(reverse('users:profile'), {
            'username': 'testuser',
            'email': 'newemail@example.com',
            'first_name': 'NewFirst',
            'last_name': 'NewLast',
        })

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertEqual(self.user.first_name, 'NewFirst')

    def test_change_password_requires_login(self):
        """Тест доступу до зміни пароля без авторизації"""
        response = self.client.get(reverse('users:change_password'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/users/login/' in response.url)

    def test_change_password_view(self):
        """Change password page test"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:change_password'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/change_password.html')

    def test_change_password_post_valid(self):
        """Valid data change password test"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(reverse('users:change_password'), {
            'old_password': 'testpass123',
            'new_password1': 'newcomplexpass123',
            'new_password2': 'newcomplexpass123',
        })

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newcomplexpass123'))

    def test_change_password_post_invalid(self):
        """Invalid data change password test"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(reverse('users:change_password'), {
            'old_password': 'wrongoldpass',
            'new_password1': 'newpass123',
            'new_password2': 'newpass123',
        })

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('testpass123'))

    def test_redirect_authenticated_from_login(self):
        """Authorized user should be redirected from login page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:login'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('news:index'))

    def test_redirect_authenticated_from_register(self):
        """Authorized user should be redirected from registration page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:register'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('news:index'))


class UserModelTestCase(TestCase):

    def test_user_creation(self):
        """User creation test"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(str(user), 'testuser')

    def test_user_profile_picture_optional(self):
        """Image optionality test"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        self.assertFalse(user.profile_picture)

    def test_superuser_creation(self):
        """Superuser creation test"""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
