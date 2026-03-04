from django import forms
from .models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'name',
            'species',
            'breed',
            'age',
            'gender',
            'description',
            'photo',
            'location',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pet name',
            }),
            'species': forms.Select(attrs={
                'class': 'form-select',
            }),
            'breed': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Breed (optional)',
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Age in years',
                'min': 0,
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about this pet...',
                'rows': 4,
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Location (city, country)',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['breed'].required = False
        self.fields['photo'].required = False
        self.fields['description'].required = False
        self.fields['location'].required = False
