from django.shortcuts import render

def homepage(request):
    """ Display the application's home page """
    return render(request, 'lmn/home.html')
