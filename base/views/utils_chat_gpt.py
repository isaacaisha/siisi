# base/views/utils_chat_gpt.py

import os
import json
import numpy as np
from scipy.spatial.distance import cosine

from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone

# Models from the same Django app
from ..models import Conversation, User

# Langchain and OpenAI integrations
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Memory handling for conversations
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory

# Language detection
from langdetect import detect

# Text-to-Speech (TTS) handling
from gtts import gTTS
from gtts.lang import tts_langs

# Load environment variables and initialize LangChain components
openai = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
llm = ChatOpenAI(temperature=0.0, model="gpt-4o")
memory = ConversationBufferMemory(k=3)

# Define a simple prompt template
prompt = PromptTemplate(input_variables=["input"], template="{input}")
conversation = LLMChain(llm=llm, memory=memory, prompt=prompt, verbose=False)
memory_summary = ConversationSummaryBufferMemory(llm=llm, max_token_limit=3)

# Define base directory and media folder path
BASE_DIR = settings.BASE_DIR
STATIC_FOLDER_PATH = os.path.join(BASE_DIR, 'static')
AUDIO_FOLDER_PATH = os.path.join(STATIC_FOLDER_PATH, 'media')
os.makedirs(AUDIO_FOLDER_PATH, exist_ok=True)


def generate_conversation_context(user_input, user_conversations):
    """Generate context from user conversations."""
    conversation_strings = [memory.conversations_summary for memory in user_conversations]
    qdocs = f"[{','.join(conversation_strings[-3:])}]"
    created_at_list = [str(memory.created_at) for memory in user_conversations]
    conversation_context = {
        "created_at": created_at_list[-3:],
        "conversations": json.loads(qdocs),
        "user_name": user_conversations[0].owner.username if user_conversations else '',
        "user_message": user_input,
    }
    return conversation_context


def handle_llm_response(user_input, conversation_context, detected_lang):
    """Handle user input and generate assistant response."""
    detected_lang = detect(user_input)
    conversation_context = adjust_conversation_context(conversation_context)
    response = get_llm_response(user_input, conversation_context)
    assistant_reply = extract_assistant_reply(response)
    assistant_reply = clean_assistant_reply(assistant_reply)
    detected_lang, flash_message = handle_language_support(detected_lang)
    audio_data = generate_audio_data(assistant_reply, detected_lang)

    memory_summary.save_context({"input": user_input}, {"output": response})
    return assistant_reply, audio_data, response, flash_message


def adjust_conversation_context(conversation_context):
    if conversation_context and 'previous_conversations' in conversation_context:
        conversation_context['previous_conversations'] = conversation_context['previous_conversations'][-3:]
    return conversation_context


def get_llm_response(user_input, conversation_context):
    if not conversation_context:
        return conversation.predict(input=user_input)
    return conversation.predict(input=json.dumps(conversation_context))


def extract_assistant_reply(response):
    if isinstance(response, str):
        return response
    if isinstance(response, dict) and 'choices' in response:
        return response['choices'][0]['message']['content']
    return None


def clean_assistant_reply(assistant_reply):
    if assistant_reply:
        return assistant_reply.replace('#', '').replace('*', '')
    return assistant_reply


def handle_language_support(detected_lang):
    flash_message = None
    if detected_lang not in tts_langs():
        flash_message = f"Language '{detected_lang}' not supported, falling back to English."
        detected_lang = 'en'
    return detected_lang, flash_message


def generate_audio_data(assistant_reply, detected_lang):
    tts = gTTS(assistant_reply, lang=detected_lang)
    audio_file_path = os.path.join(AUDIO_FOLDER_PATH, 'interface_temp_audio.mp3')
    tts.save(audio_file_path)
    with open(audio_file_path, 'rb') as audio_file:
        return audio_file.read()


def find_most_relevant_conversation(user_query, embeddings):
    query_embedding = openai.embed_query(user_query)
    similarities = [1 - cosine(query_embedding, embedding) for embedding in embeddings]
    most_similar_index = np.argmax(similarities)
    return most_similar_index, similarities[most_similar_index]


def save_to_database(user, user_input, response, audio_data):
    # Ensure user is resolved and authenticated
    if not isinstance(user, User) or not user.is_authenticated:
        return JsonResponse({"error": "Invalid user"}, status=403)

    # Save logic goes here
    # Generate embedding for the user message
    embedding = openai.embed_query(user_input)

    # Convert embedding to bytes for storage
    embedding_bytes = np.array(embedding).tobytes()

    # Prepare the memory summary and save context
    conversations_summary = memory_summary.load_memory_variables({})
    conversations_summary_str = json.dumps(conversations_summary)

    created_at = timezone.now()
    
    new_conversation = Conversation(
        user_name=user.username,
        owner=user,
        user_message=user_input,
        llm_response=response,
        audio_datas=audio_data,
        embedding=embedding_bytes,
        conversations_summary=conversations_summary_str,
        created_at=created_at
    )

    print(f'Saving to database:\n'
          f'owner_id: {new_conversation.owner_id}\n'
          f'user_name: {new_conversation.user_name}\n'
          f'user_message: {new_conversation.user_message}\n\n'
          f'llm_response: {new_conversation.llm_response}\n\n'
          f'conversations_summary: {new_conversation.conversations_summary}\n\n'
          f'created_at: {created_at}') 

    try:
        new_conversation.save()
        memory_summary.clear()
    except Exception as e:
        return JsonResponse({"error": f"Failed to save to database: {str(e)}"}, status=500)

    memory_buffer = memory.buffer_as_str
    memory_load = memory.load_memory_variables({})
    return JsonResponse({
        "memory_buffer": memory_buffer,
        "memory_load": memory_load,
    })
