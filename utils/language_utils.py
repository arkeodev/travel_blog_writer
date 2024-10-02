from googletrans import Translator


def translate_content(content: str, target_language: str) -> str:
    """
    Translate the given content to the target language.
    """
    translator = Translator()
    translated = translator.translate(content, dest=target_language)
    return translated.text
