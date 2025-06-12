# your_app/views.py

import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from .models import TextSumm, Note


def home(request):
    textsumm = TextSumm.objects.all()
    return render(request, 'home.html', {'textsumm': textsumm})
    
    
def view_text(request, pk):
    item = get_object_or_404(TextSumm, pk=pk)

    # Fetch “notes” in ascending order of creation time:
    notes = Note.objects.filter(
        user=request.user,
        textsumm=item
    ).order_by("created_at")

    return render(request, "view_text.html", {
        "item":  item,
        "notes": notes,
    })


def save_note(request, textsumm_id):
    """
    AJAX endpoint to create a new Note for the logged-in user & specified TextSumm.
    Expects JSON: { "content": "...", "sharePublicly": true/false }
    Returns JSON on success: { "success": true, "note_id": <id>, "created_at": "<iso-format>" }
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)

    content = data.get('content', '').strip()
    if not content:
        return JsonResponse({'success': False, 'error': 'Content cannot be empty.'}, status=400)

    textsumm = get_object_or_404(TextSumm, pk=textsumm_id)

    note = Note.objects.create(
        user=request.user,
        textsumm=textsumm,
        content=content,
    )

    return JsonResponse({
        'success':    True,
        'note_id':    note.id,
        'created_at': note.created_at.isoformat(),
        'content':    note.content,
    })


def edit_note(request, note_id):
    """
    AJAX endpoint to update an existing note’s content & is_public flag.
    Expects JSON: { "content": "...", "sharePublicly": true/false }
    Only the note’s owner may edit. Returns { "success": true } or error JSON.
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    note = get_object_or_404(Note, pk=note_id, user=request.user)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)

    content = data.get('content', '').strip()
    if not content:
        return JsonResponse({'success': False, 'error': 'Content cannot be empty.'}, status=400)

    note.content = content
    note.save()

    return JsonResponse({'success': True})

def get_note(request, note_id):
    """
    AJAX endpoint to fetch a single note’s content & is_public flag,
    so the “Edit” button can prefill the modal.
    URL: GET /notes/<note_id>/
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    # Only allow the note’s owner to fetch it
    note = get_object_or_404(Note, pk=note_id, user=request.user)

    return JsonResponse({
        "success":   True,
        "content":   note.content,
    })

def delete_note(request, note_id):
    """
    AJAX endpoint to delete a note. Only the owner may delete.
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    note = get_object_or_404(Note, pk=note_id, user=request.user)
    note.delete()
    return JsonResponse({'success': True})
