from django.test import TestCase # extention of TestCase that is specific to testing Django applications
from django.urls import reverse # used to get the URL for a view by its name
# Create your tests here.

from .models import Place

class TestHomePage(TestCase):
    def test_home_page_shows_empty_list_message_for_empty_database(self):
        home_page_url = reverse('place_list') # get the URL for the home page
        response = self.client.get(home_page_url) # reverse gets the URL for the view with the name 'place_list'
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist.')

class TestWishList(TestCase):

    fixtures = ['test_places']
    #only failing test TODO: troubleshoot
    def test_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')

class TestVisitedPage(TestCase):

    def test_visited_page_shows_empty_list_message_for_empty_database(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'You haven\'t visited any places yet.')


class VisitedList(TestCase):
    fixtures = ['test_places']

    def test_visited_list_contains_visited_places(self): # converts path name to url
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')

class TestAddNewPlace(TestCase):

    def test_add_new_unvisited_place(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}

        response = self.client.post(add_place_url, new_place_data, follow=True) # follow true means that if the view redirects, the test client will follow the redirect and return the response from the final view
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        response_places = response.context['places'] # get the places from the context of the response
        self.assertEqual(1, len(response_places)) # check only one place
        tokyo_from_response = response_places[0] # get the first place

        tokyo_from_database = Place.objects.get(name='Tokyo', visited=False) # get the place from the database

        self.assertEqual(tokyo_from_response, tokyo_from_database) # check that the place from the response is the same as the place from the database


class TestVisitPlace(TestCase):

    fixtures = ['test_places']

    def test_visit_place(self):
        visit_place_url = reverse('place_was_visited', args=(2, )) # args is a tuple of the arguments to pass to the view
        response = self.client.post(visit_place_url, follow=True) # not sending data. stays in the url
        
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        self.assertNotContains(response, 'New York') # check that New York is not in the response
        self.assertContains(response, 'Tokyo') # check that Tokyo is in the response

        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited) # check that New York is now visited

    def test_visit_non_existent_place(self):
        visit_non_existant_place_url = reverse('place_was_visited', args=(123456, ))
        response = self.client.post(visit_non_existant_place_url, follow=True)
        self.assertEqual(404, response.status_code)