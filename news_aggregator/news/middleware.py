from django.utils import translation
from django.conf import settings


class TranslationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = request.session.get('django_language')
        if not language:
            language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, 'en')

        translation.activate(language)
        request.LANGUAGE_CODE = language

        response = self.get_response(request)
        translation.deactivate()

        return response
