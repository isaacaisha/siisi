# base/views/utils_gpt_convers.py

import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils import timezone

from dataclasses import dataclass
from typing import Optional

from ..forms import ConversationIdForm, DeleteForm
from ..models import Conversation


@dataclass
class ConversationFilters:
    owner_id: int
    limit: Optional[int] = None
    offset: int = 0
    search: Optional[str] = None
    order_by_desc: bool = False
    liked_value: Optional[int] = None


def validate_filters(filters: ConversationFilters):
    """Validate and convert limit and offset to integers or None."""
    try:
        filters.limit = int(filters.limit) if filters.limit and str(filters.limit).isdigit() else None
    except ValueError:
        filters.limit = None

    try:
        filters.offset = int(filters.offset) if filters.offset and str(filters.offset).isdigit() else 0
    except ValueError:
        filters.offset = 0
    return filters


def get_conversations(filters: ConversationFilters):
    """Fetch conversations based on provided filters."""
    filters = validate_filters(filters)
    query_params = {
        'owner_id': filters.owner_id,
        'liked': filters.liked_value,
    }

    query = Conversation.objects.filter(**{k: v for k, v in query_params.items() if v is not None})

    if filters.search:
        query = query.filter(user_message__icontains=filters.search.strip())
    if filters.order_by_desc:
        query = query.order_by('-id')
    if filters.limit is not None:
        query = query[filters.offset:filters.offset + filters.limit]
    elif filters.offset:
        query = query[filters.offset:]

    return query.all()


def serialize_conversation(conversation, last_summary_only=True):
    """Convert conversation instance to dictionary format."""
    summary = conversation.conversations_summary.split('\n')[-1] if last_summary_only else conversation.conversations_summary
    return {
        "id": conversation.id,
        "owner_id": conversation.owner.id,
        "user_name": conversation.user_name,
        "user_message": conversation.user_message,
        "llm_response": conversation.llm_response,
        "conversations_summary": summary,
        "created_at": conversation.created_at.strftime("%a %d %B %Y %H:%M:%S"),
        "liked": conversation.liked,
    }


def render_conversation_template(request, template_name: str, context: dict):
    """Render template with context."""
    return render(request, template_name, context)


@login_required(login_url='login')
def allConversations(request):
    owner_id = request.user.id
    filters = ConversationFilters(
        owner_id=owner_id,
        limit=request.GET.get('limit'),
        offset=request.GET.get('offset'),
        search=request.GET.get('search'),
        order_by_desc=True
    )
    
    conversations = get_conversations(filters)
    serialized_conversations = [serialize_conversation(conversation) for conversation in conversations]
    total_conversations = Conversation.objects.filter(owner_id=owner_id).count()
    
    context = {
        "filters": filters,
        "current_user": request.user,
        "conversations": serialized_conversations,
        "total_conversations": total_conversations,
        "limit": filters.limit,
        "offset": filters.offset,
        "search": filters.search,
        'date': timezone.now().strftime(_("%a %d %B %Y")),
    }

    # Check if no conversations are found and set the search message
    if not serialized_conversations:
        context["search_message"] = _("No conversations found for search term: '{filters.search}'").format(filters.search)

    return render_conversation_template(request, 'base/conversation_all.html', context)


@login_required(login_url='login')
def likedConversations(request):
    owner_id = request.user.id
    filters = ConversationFilters(
        owner_id=request.user.id,
        limit=request.GET.get('limit', 3),
        offset=request.GET.get('offset', 0),
        search=request.GET.get('search', None),
        order_by_desc=True,
        liked_value=1
    )

    liked_conversations = get_conversations(filters)
    serialized_liked_conversations = [serialize_conversation(conversation) for conversation in liked_conversations]
    total_conversations_liked = Conversation.objects.filter(owner_id=owner_id, liked=1).count()

    context = {
        "filters": filters,
        "current_user": request.user,
        "liked_conversations": serialized_liked_conversations,
        "total_conversations_liked": total_conversations_liked,
        "liked_conversations_count": len(liked_conversations),
        "limit": filters.limit,
        "offset": filters.offset,
        "search": filters.search,
        'date': timezone.now().strftime(_("%a %d %B %Y")),
    }

    # Check if no conversations are found and set the search message
    if not serialized_liked_conversations:
        context["search_message"] = _("No conversations found for search term: '{filters.search}'").format(filters.search)

    return render_conversation_template(request, 'base/conversations_liked.html', context)


def updateLike(request, conversation_id):
    if request.method == 'POST':
        try:
            liked = json.loads(request.body).get('liked')
            conversation = get_object_or_404(Conversation, pk=conversation_id)
            conversation.liked = liked
            conversation.save()
            return JsonResponse({'message': _('Liked status updated successfully')}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': _('Invalid request method')}, status=405)


@login_required(login_url='login')
def ConversationById(request):
    select_conversation_form = ConversationIdForm(request.POST or None)
    context = {
        'select_conversation_form': select_conversation_form,
        'current_user': request.user,
        'date': timezone.now().strftime(_("Date format: %a %d %B %Y")),
    }

    if request.method == "POST" and select_conversation_form.is_valid():
        selected_conversation_id = select_conversation_form.cleaned_data['conversation_id']
        return redirect('conversation_selected', conversation_id=selected_conversation_id)
    
    return render(request, 'base/conversation_by_id.html', context)


@login_required(login_url='login')
def ConversationSelected(request, conversation_id):
    conversation_ = get_object_or_404(Conversation, pk=conversation_id)
    context = {
        'current_user': request.user,
        'conversation_id': conversation_id,
        'conversation': conversation_,
        'date': timezone.now().strftime(_("%a %d %B %Y")),
    }
    
    if conversation_.owner_id != request.user.id:
        return render(request, 'conversation_forbidden.html', context)
    else:
        return render(request, 'base/conversation_selected.html', context)


@login_required(login_url='login')
def deleteConversation(request):
    delete_conversation_form = DeleteForm()
    context = {
        'current_user': request.user,
        'delete_conversation_form': delete_conversation_form,
        'date': timezone.now().strftime(_("%a %d %B %Y")),
    }
    
    if request.method == "POST":
        if delete_conversation_form.is_valid():
            conversation_id = delete_conversation_form.cleaned_data['conversation_id']
            conversation_to_delete = get_object_or_404(Conversation, pk=conversation_id)
            
            if conversation_to_delete.owner_id != request.user.id:
                context['conversation_id'] = conversation_id
                return render(request, 'base/conversation_forbidden.html', context)
            else:
                conversation_to_delete.delete()
                messages.success(request, _(
                    "Conversation with ID: 🔥{conversation_id}🔥 deleted 😎"
                    ).format(conversation_id=conversation_id)
                    )
                return redirect('delete_conversation')
                
    return render(request, 'base/conversation_delete.html', context)
