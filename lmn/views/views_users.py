from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from ..forms import NoteSearchForm, UserRegistrationForm, ProfileForm
from ..models import Note, Profile


def user_profile(request, user_pk):
    """ Get user profile for any user on the site. 
    Any user may view any other user's profile. 
    """
    
    """
    TODO
    1. create form instance
    2. GET search string from template's form instance (passed by view)
    3. if search string exists, filter list of instances of notes that match search string and contextualize; if not, contextualize list of all instances
    4. contextualize user_pk iot fetch right template + action url
    """

    user = User.objects.get(pk=user_pk)

    form = NoteSearchForm()
    search_text = request.GET.get('search_text')  # template form
    if search_text:
        notes1 = Note.objects.filter(user=user.pk, text__icontains=search_text).order_by('-posted_date')
        notes2 = Note.objects.filter(user=user.pk, title__icontains=search_text).order_by('-posted_date')
        notes = notes1 | notes2
    else:
        notes = Note.objects.filter(user=user.pk).order_by('-posted_date')

    # Get profile if it exists
    profile = Profile.objects.filter(user=user).first()

    return render(request, 'lmn/users/user_profile.html', {'user_profile': user, 'notes': notes , 'profile': profile, 'search_text': search_text, 'form': form})


@login_required
def my_user_profile(request):
    """ Get the currently logged-in user's profile """
    # TODO - editable version for logged-in user to edit their own profile
    return redirect('user_profile', user_pk=request.user.pk)


@login_required
def edit_profile(request):
    """ Edit current user's profile """
    # Get the current user's profile, or create one if doesn't exist
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Load the form with submitted data and the current profile
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('user_profile', user_pk=request.user.pk)

    else:
        # Load the form with the user's existing profile data
        form = ProfileForm(instance=profile)

    return render(request, 'lmn/users/edit_profile.html', {'form': form})


def register(request):
    """ Handles user registration flow

    GET request - show a user registration form.
    POST request - register a new user
    """

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            if user:
                login(request, user)
                return redirect('user_profile', user_pk=request.user.pk)
            else:
                messages.add_message(request, messages.ERROR, 'Unable to log in new user')
        else:
            messages.add_message(request, messages.INFO, 'Please check the data you entered')
            # include the invalid form, which will have error messages added to it. 
            # The error messages will be displayed by the template.
            return render(request, 'registration/register.html', {'form': form})

    form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
