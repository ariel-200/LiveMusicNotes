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
        # Filter shows by artist OR venue name (case-insensitive)
        past_shows = Show.objects.filter(
            Q(artist__name__icontains=search_name) |
            Q(venue__name__icontains=search_name),
            show_date__lte=now
        ).order_by('-show_date')  # Most recent past shows first

        upcoming_shows = Show.objects.filter(
            Q(artist__name__icontains=search_name) |
            Q(venue__name__icontains=search_name),
            show_date__gt=now
        ).order_by('show_date')  # Soonest upcoming shows first

    else:
        # No search term, show all shows
        past_shows = Show.objects.filter(show_date__lte=now).order_by('-show_date')
        upcoming_shows = Show.objects.filter(show_date__gt=now).order_by('show_date')

    return render(request, 'lmn/shows/show_list.html', {
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'search_term': search_name
    })
