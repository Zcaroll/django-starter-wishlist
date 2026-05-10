from django.db import models

# Create your models here.

class Place(models.Model):
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)

    def __str__(self):
        # not displayed to user, but might be helpful for the dev
        return f'{self.name} (Visited: {self.visited})'