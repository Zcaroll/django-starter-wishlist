from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Create your views here.

# called by django and given information about the request
def place_list(request):

    if request.method == 'POST': 
        #create new place
        form = NewPlaceForm(request.POST) 
        place = form.save(commit=False) #makes a model object from form
        place.user = request.user # associate the place with the current user
        if form.is_valid(): # validation against database constraints
            place.save() # save the new place to the database
            return redirect('place_list') # reloads home page
        

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name') # get all places from the database that are not visited; filter by user
    new_place_form = NewPlaceForm() # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True) 
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

@login_required
def place_was_visited(request, place_pk): #pk is primary key
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk) # get the place from the database
        place = get_object_or_404(Place, pk=place_pk) # get the place from the database; if it doesn't exist, return 404 error
        # prevents malicious user from marking a place as visited if it does not belong to them
        if place.user == request.user: # if the place does not belong to the current user, return 403 error
            place.visited = True # change visited to true
            place.save() # save the change to the database
        else:
            return HttpResponseForbidden() # return 403 error if the place does not belong to the current user


    # return ridirect('places_visited') # directs to places visited page
    return redirect('place_list') # name of path; redirect to wishlist


def about(request):
    author = 'Zach'
    about = 'A website of a wishlist of places I want to visit.'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk) # get the place from the database; if it doesn't exist, return 404 error
    return render(request, 'travel_wishlist/place_details.html', {'place': place})

@login_required
# allows user to delete a place from the database
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk) 
    if place.user == request.user: 
          place.delete() 
          return redirect('place_list') 
    else:
          return HttpResponseForbidden() 