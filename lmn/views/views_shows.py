from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count

from ..models import Show


def show_list(request):
    """ Display past and upcoming shows """
    now = timezone.now()

    past_shows = Show.objects.filter(show_date__lte=now).order_by('-show_date')
    upcoming_shows = Show.objects.filter(show_date__gt=now).order_by('show_date')

    return render(request, 'lmn/shows/show_list.html', {
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows
    })

def shows_top(request):
    """ Display shows ordered by notes descending """

    # shows list ordered by number of notes; limit to certain number of top shows
    shows_top_count = 10;
    shows = Show.objects.annotate(num_notes=Count('note')).order_by('-num_notes')[:shows_top_count]

    return render(request, 'lmn/shows/shows_top.html', {'shows': shows, 'shows_top_count': shows_top_count})
