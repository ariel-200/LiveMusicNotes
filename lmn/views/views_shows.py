from django.shortcuts import render
from django.utils import timezone

from ..models import Show


def show_list(request):
    """ Display past and upcoming shows """
    now = timezone.now()

    past_shows = Show.objects.filter(show_date__lte=now).order_by('-show_date')
    upcoming_shows = Show.objects.filter(show_date__gt=now).order_by('show_date')

    return render(request, 'lmn/show_list.html', {
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows
    })