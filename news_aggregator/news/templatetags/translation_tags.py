from django import template

register = template.Library()

TRANSLATIONS = {
    'uk': {
        'Search': 'Пошук',
        'Settings': 'Налаштування',
        'Profile': 'Профіль',
        'Logout': 'Вийти',
        'Interface Language': 'Мова інтерфейсу',
        'Close': 'Закрити',
        'Log In': 'Увійти',
        'Sign In': 'Увійти',
        'Email': 'Електронна пошта',
        'Password': 'Пароль',
        'Username': 'Імʼя користувача',
        'Forgot password?': 'Забули пароль?',
        "Don't have an account?": 'Немає облікового запису?',
        'Create': 'Створити',
        'Sign Up': 'Зареєструватися',
        'Confirm Password': 'Підтвердіть пароль',
        'Register': 'Зареєструватися',
        'Have an account?': 'Вже є обліковий запис?',
        'Log in': 'Увійти',
        'Main Page': 'Головна',
        'Read Later': 'Читати пізніше',
        'Filters': 'Фільтри',
        'Category': 'Категорія',
        'Source': 'Джерело',
        'All Categories': 'Усі категорії',
        'All Sources': 'Усі джерела',
        'Clear Filters': 'Очистити фільтри',
        'General': 'Загальне',
        'Business': 'Бізнес',
        'Technology': 'Технології',
        'Entertainment': 'Розваги',
        'Health': 'Здоровʼя',
        'Science': 'Наука',
        'Sports': 'Спорт',
        'Previous': 'Попередня',
        'Next': 'Наступна',
        'No news found.': 'Новини не знайдено.',
        'Please log in to save articles.': 'Будь ласка, увійдіть, щоб зберігати статті.',
        'Back': 'Назад',
        'Add to read later': 'Додати до списку',
        'Saved': 'Збережено',
        'Translate this news': 'Перекласти цю новину',
        'Select language': 'Оберіть мову',
        'Original': 'Оригінал',
        'Read full article on source': 'Читати повну статтю на сайті джерела',
        'Remove from list?': 'Видалити зі списку?',
        'Your reading list is empty.': 'Ваш список для читання порожній.',
        'Edit Profile': 'Редагувати профіль',
        'First Name': 'Імʼя',
        'Last Name': 'Прізвище',
        'Save Changes': 'Зберегти зміни',
        'Change Password': 'Змінити пароль',
        'Cancel': 'Скасувати',
        'Old Password': 'Старий пароль',
        'New Password': 'Новий пароль',
        'Confirm New Password': 'Підтвердіть новий пароль',
        'Reset Password': 'Скинути пароль',
        'Send Reset Link': 'Надіслати посилання',
        'Back to Login': 'Назад до входу',
        'Account': 'Обліковий запис',
        'Note': 'Примітка',
        'Full article content is available on the source website.': 'Повний текст статті доступний на сайті джерела.',
        'Preview content is not available. Please visit the source website to read the full article.': 'Передпоказ статті не доступний. Перейдіть на сайт джерела, щоб прочитати повний текст статті.',
        'Check Your Email': 'Перевірте свою пошту',
        'We have sent you an email with instructions to reset your password. Please check your inbox.': 'Ми надіслали вам листа з інструкціями для скидання пароля. Будь ласка, перевірте свою поштову скриньку.',
        'Set New Password': 'Встановити новий пароль',
        'Invalid Link': 'Недійсне посилання',
        'The password reset link is invalid or has expired.': 'Посилання для скидання пароля недійсне або прострочене.',
        'Request New Link': 'Запросити нове посилання',
        'Password Reset Complete': 'Скидання пароля завершено',
        'Your password has been successfully reset. You can now log in with your new password.': 'Ваш пароль успішно скинуто. Тепер ви можете увійти з новим паролем.',
        'Enter your email address and we will send you a link to reset your password.': 'Введіть свою електронну адресу, і ми надішлемо вам посилання для скидання пароля.',
    }
}


@register.simple_tag(takes_context=True)
def t(context, text):
    """Tag for text translation in templates"""
    request = context.get('request')
    if not request:
        return text

    language = getattr(request, 'LANGUAGE_CODE', 'en')

    if language == 'en':
        return text

    return TRANSLATIONS.get(language, {}).get(text, text)
