from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q

from ..models import Show


def show_list(request):
    """ Display past and upcoming shows

    If request contains a GET parameter search_name then
    only include shows with artist or venue names containing that text.

    """
    now = timezone.now()

    # Get search term from request
    search_name = request.GET.get('search_name')

    if search_name:
        ignored_words = ['at', 'the', 'an', 'a']
        search_words = [
            word for word in search_name.strip().split()
            if word.lower() not in ignored_words
        ]

        # Most recent past shows first
        past_shows = Show.objects.filter(show_date__lte=now).order_by('-show_date')
        # Soonest upcoming shows first
        upcoming_shows = Show.objects.filter(show_date__gt=now).order_by('show_date')

        # Each word must match either the artist or venue name
        for word in search_words:
            past_shows = past_shows.filter(
                Q(artist__name__icontains=word) |
                Q(venue__name__icontains=word)
            )

            upcoming_shows = upcoming_shows.filter(
                Q(artist__name__icontains=word) |
                Q(venue__name__icontains=word)
            )

    else:
        # No search term, show all shows
        past_shows = Show.objects.filter(show_date__lte=now).order_by('-show_date')
        upcoming_shows = Show.objects.filter(show_date__gt=now).order_by('show_date')

    return render(request, 'lmn/shows/show_list.html', {
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'search_term': search_name
    })
