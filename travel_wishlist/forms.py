from django import forms
from .models import Place

class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'visited']


# user's custom date input from django
class DateInput(forms.DateInput):
    input_type = 'date'

# form for trip review; allows user to enter notes, date visited, and upload a photo
class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'visited', 'notes', 'date_visited', 'photo']
        widgets = {
            'date_visited': DateInput(),
        }