from django.shortcuts import render
from django.utils import timezone

from ..models import Note, Show

def homepage(request):
    """ Display the application's home page """

    recent_shows = Show.objects.filter(show_date__lte=timezone.now()
                                       ).order_by('-show_date')[:5]

    latest_notes = Note.objects.all().order_by('-posted_date')[:5]

    return render(request, 'lmn/home.html', {
        'recent_shows': recent_shows,
        'latest_notes': latest_notes,
    })
