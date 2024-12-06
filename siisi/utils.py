# siisi/utils.py

from django.utils.translation import activate
from siisi.middleware import get_current_request


def activate_current_language():
    """
    Activates the current language based on the LANGUAGE_CODE in the request.
    """
    current_request = get_current_request()
    if current_request:
        lang = getattr(current_request, 'LANGUAGE_CODE', None)
        if lang:
            activate(lang)
