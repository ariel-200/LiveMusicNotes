from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

# Remember that every model gets a primary key field by default.

# The User model is provided by Django. The email field is not unique by
# default, so add this to prevent more than one user with the same email.
User._meta.get_field('email')._unique = True

# And, require email, first name, and last name for each user
User._meta.get_field('email')._blank = False
User._meta.get_field('last_name')._blank = False
User._meta.get_field('first_name')._blank = False


class Artist(models.Model):
    """ Represents a musician or a band - a music artist """

    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return f'Name: {self.name}'


class Venue(models.Model):
    """ Represents a place that Shows take place at. """

    name = models.CharField(max_length=200, blank=False, unique=True)
    city = models.CharField(max_length=200, blank=False)
    state = models.CharField(max_length=2, blank=False)

    def __str__(self):
        return f'Name: {self.name} Location: {self.city}, {self.state}'


class Show(models.Model):
    """ One Artist playing at one Venue at a particular date and time. """

    show_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    # validation
    def clean(self):
        super().clean()

        # check that start and end datetimes exist
        if self.show_date and self.end_date:

            # check correct start and end
            if self.end_date <= self.show_date:
                raise ValidationError({'end_date': 'Error: End datetime cannot be earlier than start datetime!'})  # will raise error in input box

            # check overlaps
            overlap = Show.objects.filter(
                show_date__lt=self.end_date,
                end_date__gt=self.show_date,
                venue=self.venue
            ).exclude(pk=self.pk).exists()

            if overlap:
                raise ValidationError('Error: Time/venue slot overlaps with existing show!')

        if not self.show_date:
            raise ValidationError({'show_date': 'Error: Invalid start datetime!'})
        if not self.end_date:
            raise ValidationError({'end_date': 'Error: Invalid end datetime!'})

    def __str__(self):
        return f'Artist: {self.artist} At: {self.venue} From: {self.show_date} To: {self.end_date}'


class Note(models.Model):
    """ One User's opinion of one Show. """
    
    show = models.ForeignKey(Show, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(max_length=1000, blank=False)
    posted_date = models.DateTimeField(auto_now_add=True, blank=False)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def clean(self):
        super().clean()

        if not self.show_id:
            return

        if self.show and self.show.show_date > timezone.now():
            raise ValidationError('Cannot add notes for future shows.')

    def __str__(self):
        return f'User: {self.user} Show: {self.show} Note title: {self.title} \
        Text: {self.text} Posted on: {self.posted_date}'

    class Meta:
        constraints =[
            models.UniqueConstraint(fields=['user', 'show'], name='unique_user_show_note')
        ]

    def save(self, *args, **kwargs):
        '''
        Overrides save to verify that images are deleted from the media directory when they are deleted fromt the database
        '''
        if self.pk:
            old_image = Note.objects.get(pk=self.pk).image
            super().save(*args, **kwargs)
            if old_image and old_image != self.image:
                old_image.delete(save=False)
        else:
            super().save(*args, **kwargs)



class Profile(models.Model):
    # Link each profile to only one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Optional fields on the profile
    bio = models.TextField(blank=True)
    favorite_artist = models.CharField(max_length=200, blank=True)
    favorite_genre = models.CharField(max_length=200, blank=True)
    # Favorite show (linked to existing Show model)
    # SET_NULL prevents errors if the show is deleted
    favorite_show = models.ForeignKey(
        Show,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
