from django.db import models
from django.contrib.auth.models import User # user from django


# Create your models here.

class Place(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE) # each place is associated with a user; if the user is deleted, the place is deleted
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True) # blank means it can be empty in the form; null means it can be null in the database
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True) # upload_to specifies the directory where the uploaded files will be stored

    def __str__(self):
        # not displayed to user, but might be helpful for the dev
        photo_str = self.photo.url if self.photo else 'No photo'
        notes_str = self.notes[100: ] if self.notes else 'No notes' # only show the first 100 characters of the notes
        return f'{self.name} (Visited: {self.visited}) on {self.date_visited}. Notes: {notes_str} - Photo: {photo_str}'
    