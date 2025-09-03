from django import forms

class LocationForm(forms.Form):
    location = forms.CharField(
        label="Enter a city or ZIP/postal code",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "e.g., Johannesburg or 2000"})
    )

