# chatgpt/views.py

import os
from datetime import timedelta

from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse

from django.utils.translation import gettext as _
from django.utils import timezone

from openai import OpenAI
from .models import ChatData

from gtts import gTTS
# Language detection
from langdetect import detect, DetectorFactory


DetectorFactory.seed = 0  # Ensures consistent language detection results

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Time limit in minutes
RATE_LIMIT_MINUTES = 3


def index(request):

    context = {
        'date': timezone.now().strftime(_("%a %d %B %Y")),
        }
    return render(request, 'chatgpt/index.html', context)




def response(request):
    if request.method == 'POST':
        try:
            # Get the message from the POST request
            message = request.POST.get('message', '')

            # If no message is provided, add an error message using Django's messages framework
            if not message:
                messages.error(request, _("No message provided"))
                return redirect('index')  # Redirect the user back to the main page (or wherever you want)

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

            # Always add invitation to register and log in
            invitation_message = _(
                " For more privileges, register and log in to access exclusive features!"
            )
            answer += invitation_message

            # Check if "rasta" or "dread" is mentioned in the message
            if "rasta" in message.lower() or "dread" in message.lower():
                contact_details = _(
                    f"\n\nYou can reach out via WhatsApp at: +34 631 06 90\n"
                    f"Instagram: [dbtevolution](https://www.instagram.com/dbtevolution)"
                )
                answer = contact_details
                print("Contact details appended to the response.")

            # Save ChatData object without user association
            new_chat = ChatData(message=message, response=answer)
            new_chat.save()
            print(f"ChatData saved with id: {new_chat.id}")

            # Convert the OpenAI response to speech
            try:
                detected_lang = detect(answer)
                print(f"Detected language: {detected_lang}")
                tts = gTTS(text=answer, lang=detected_lang)
                audio_path = os.path.join(settings.MEDIA_ROOT, f'response_{new_chat.id}.mp3')
                tts.save(audio_path)
            except Exception as e:
                print(f"Error generating audio: {e}")
                audio_path = None

            audio_url = request.build_absolute_uri(settings.MEDIA_URL + f'response_{new_chat.id}.mp3') if audio_path else None
            return JsonResponse({'response': answer, 'audio_url': audio_url})

        except Exception as e:
            print(f"Error processing request: {e}")
            return JsonResponse({'error': str(e)}, status=500)
