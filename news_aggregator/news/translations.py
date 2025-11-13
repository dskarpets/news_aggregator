from googletrans import Translator


class TranslationService:
    """Text translation service"""

    @staticmethod
    def translate_article(article_data, dest_lang='uk'):
        """News article translation method"""
        translated = article_data.copy()

        try:
            translator = Translator()

            if article_data.get('title'):
                translated['title'] = translator.translate(
                    article_data['title'],
                    dest=dest_lang
                ).text

            if article_data.get('description'):
                translated['description'] = translator.translate(
                    article_data['description'],
                    dest=dest_lang
                ).text

            if article_data.get('content'):
                translated['content'] = translator.translate(
                    article_data['content'],
                    dest=dest_lang
                ).text

            return translated
        except Exception as e:
            print(f'Article translation error: {e}')
            return article_data


TRANSLATION_LANGUAGES = [
    ('uk', 'Українська'),
    ('en', 'English'),
    ('fr', 'Français'),
    ('de', 'Deutsch'),
    ('es', 'Español'),
    ('it', 'Italiano'),
    ('pl', 'Polski'),
]
