import os

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

from django.utils.translation import gettext as _, activate, get_language
from siisi.middleware import get_current_request  

from openai import OpenAI
from .models import ChatData

from gtts import gTTS
from django.utils import timezone

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def index(request):
    #activate('es')  # Force Spanish
    # Get current language from request
    current_request = get_current_request()
    if current_request:
        lang = current_request.LANGUAGE_CODE
        activate(lang)  # Activate the language for translations


    print(f"LANGUAGE_CODE: {request.LANGUAGE_CODE}")  # Debug language code
    print(f"Available Languages: {settings.LANGUAGES}")  # Confirm languages
    print(f"Current Request: {get_current_request()}")

    output = _("Welcome to my site.")
    context = {
        'output': output,
        'date': timezone.now().strftime("%a %d %B %Y"),
        }
    
    print(_('Hello, World!')) 
    return render(request, 'chatgpt/index.html', context)


def response(request):
    # Get current language from request
    current_request = get_current_request()
    if current_request:
        lang = current_request.LANGUAGE_CODE
        activate(lang)  # Activate the language for translations

    if request.method == 'POST':
        message = request.POST.get('message', '')

        # Log the received message
        print(f"Message received: {message}")

        # Generate OpenAI response
        completion = client.chat.completions.create(
            model='gpt-4',
            messages=[
                {"role": "system", "content": _("You are a helpful assistant.")},
                {"role": "user", "content": message}
            ]
        )
        answer = completion.choices[0].message.content
        print(f"Answer generated: {answer}")

        # Save ChatData object without user association
        new_chat = ChatData(message=message, response=answer)
        new_chat.save()
        print(f"ChatData saved with id: {new_chat.id}")

        # Convert the OpenAI response to speech
        try:
            tts = gTTS(text=answer, lang=get_language())  # Use the active language
            audio_path = os.path.join(settings.MEDIA_ROOT, f'response_{new_chat.id}.mp3')
            tts.save(audio_path)
        except Exception as e:
            print(f"Error generating audio: {e}")
            audio_path = None

        # Return JSON response including audio URL
        audio_url = request.build_absolute_uri(settings.MEDIA_URL + f'response_{new_chat.id}.mp3') if audio_path else None
        return JsonResponse({'response': answer, 'audio_url': audio_url})
