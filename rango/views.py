from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # Construct a dictionary to pass to the template engine as its content
    # Note the key boldmessage matches to {{ boldmessage }} in the template
    context_dict = {'boldmessage' : 'Crunchy, creamy, cookie, candy, cupcake!'}

    # Return a rendered response to the client
    # We make use of the shortcut function to make our lives easier
    # Note the first parameter is the template we wish to use
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return HttpResponse("Rango says here is the about page.<a href='/rango/'>Index</a>")

