import os

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

from openai import OpenAI
from .models import ChatData

from gtts import gTTS
from django.utils import timezone


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def index(request):
    context = {
        'date': timezone.now().strftime("%a %d %B %Y"),
        }
    return render(request, 'chatgpt/index.html', context)


def response(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')

        # Log the received message
        print(f"Message received: {message}")

        # Generate OpenAI response
        completion = client.chat.completions.create(
            model='gpt-4',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
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
            tts = gTTS(text=answer, lang='en')
            audio_path = os.path.join(settings.MEDIA_ROOT, f'response_{new_chat.id}.mp3')
            tts.save(audio_path)
        except Exception as e:
            print(f"Error generating audio: {e}")
            audio_path = None

        # Return JSON response including audio URL
        audio_url = request.build_absolute_uri(settings.MEDIA_URL + f'response_{new_chat.id}.mp3') if audio_path else None
        return JsonResponse({'response': answer, 'audio_url': audio_url})
