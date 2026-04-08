""" Views related to creating and viewing Notes for shows. """

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from ..models import Note, Show
from ..forms import NewNoteForm 


@login_required
def new_note(request, show_pk):
    """ Create a new note for a show. """
    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST':
        form = NewNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.show = show
            note.save()
            return redirect('note_detail', note_pk=note.pk)
    else:
        form = NewNoteForm()

    return render(request, 'lmn/notes/new_note.html', {'form': form, 'show': show})


def latest_notes(request):
    """ Get the 20 most recent notes, ordered with most recent first. """
    notes = Note.objects.all().order_by('-posted_date')[:20]   # slice of the 20 most recent notes
    return render(request, 'lmn/notes/note_list.html', {'notes': notes, 'title': 'Latest Notes'})


def notes_for_show(request, show_pk): 
    """ Get notes for one show, most recent first. """
    show = get_object_or_404(Show, pk=show_pk)  
    notes = Note.objects.filter(show=show_pk).order_by('-posted_date')
    return render(request, 'lmn/notes/notes_for_show.html', {'show': show, 'notes': notes})


def note_detail(request, note_pk):
    """ Display one note. """
    note = get_object_or_404(Note, pk=note_pk)
    return render(request, 'lmn/notes/note_detail.html', {'note': note})
