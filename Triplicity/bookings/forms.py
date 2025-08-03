from django import forms

class BookingForm(forms.Form):
    person_count = forms.IntegerField(min_value=1, label='Number of Persons', widget=forms.NumberInput(attrs={
        'class': 'form-control', 'style': 'max-width: 150px;'
    }))
