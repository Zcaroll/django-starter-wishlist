from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.

# called by django and given information about the request
def place_list(request):

    if request.method == 'POST': 
        #create new place
        form = NewPlaceForm(request.POST) 
        place = form.save() #makes a model object from form
        if form.is_valid(): # validation against database constraints
            place.save() # save the new place to the database
            return redirect('place_list') # reloads home page
        

    places = Place.objects.all() # get all the objects from the database
    new_place_form = NewPlaceForm() # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})


def places_visited(request):
    visited = Place.objects.filter(visited=True) 
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

def place_was_visited(request, place_pk): #pk is primary key
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk) # get the place from the database
        place = get_object_or_404(Place, pk=place_pk) # get the place from the database; if it doesn't exist, return 404 error
        place.visited = True # change visited to true
        place.save() # save the change to the database

    # return ridirect('places_visited') # directs to places visited page
    return redirect('place_list') # name of path; redirect to wishlist


def about(request):
    author = 'Zach'
    about = 'A website of a wishlist of places I want to visit.'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})