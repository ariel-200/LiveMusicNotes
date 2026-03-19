from django.urls import path
from django.contrib.auth import views as auth_views

from .views import views_main, views_artists, views_venues, views_notes, views_users


urlpatterns = [

    path('', views_main.homepage, name='homepage'),

    # Venue related URLs
    path('venues/list/', views_venues.venue_list, name='venue_list'),
    path('venues/detail/<int:venue_pk>/', views_venues.venue_detail, name='venue_detail'),
    path('venues/artists_at/<int:venue_pk>/', views_venues.artists_at_venue, name='artists_at_venue'),

    # Note related URLs
    path('notes/latest/', views_notes.latest_notes, name='latest_notes'),
    path('notes/detail/<int:note_pk>/', views_notes.note_detail, name='note_detail'),
    path('notes/for_show/<int:show_pk>/', views_notes.notes_for_show, name='notes_for_show'),
    path('notes/add/<int:show_pk>/', views_notes.new_note, name='new_note'),

    # Artist related URLs
    path('artists/list/', views_artists.artist_list, name='artist_list'),
    path('artists/detail/<int:artist_pk>/', views_artists.artist_detail, name='artist_detail'),
    path('artists/venues_played/<int:artist_pk>/', views_artists.venues_for_artist, name='venues_for_artist'),

    # User related URLs
    path('user/profile/<int:user_pk>/', views_users.user_profile, name='user_profile'),
    path('user/profile/', views_users.my_user_profile, name='my_user_profile'),

    # Account related URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='lmn/home.html'), name='logout'),
    path('register/', views_users.register, name='register'),

]
