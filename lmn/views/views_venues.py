from django.shortcuts import render, get_object_or_404

from ..models import Venue, Show
from ..forms import VenueSearchForm

from django.core.paginator import Paginator

def venue_list(request):
    """ Get a list of all venues, ordered by name.

    If request contains a GET parameter search_name then 
    only include venues with names containing that text. """

    form = VenueSearchForm()
    search_name = request.GET.get('search_name')

    if search_name:
        # search for this venue, display results. Use case-insensitive contains
        venues = Venue.objects.filter(name__icontains=search_name).order_by('name')
    else:
        venues = Venue.objects.all().order_by('name')

    paginator = Paginator(venues, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'lmn/venues/venue_list.html', {
        'venues': page_obj,
        'page_obj': page_obj,
        'form': form,
        'search_term': search_name
        })

def artists_at_venue(request, venue_pk):  
    """ Get all of the artists who have played a show at the venue with the pk provided """
    shows = Show.objects.filter(venue=venue_pk).order_by('-show_date') 
    venue = Venue.objects.get(pk=venue_pk)

    return render(request, 'lmn/artists/artist_list_for_venue.html', {'venue': venue, 'shows': shows})


def venue_detail(request, venue_pk):
    """ Get details about a venue """
    venue = get_object_or_404(Venue, pk=venue_pk)
    return render(request, 'lmn/venues/venue_detail.html', {'venue': venue})
