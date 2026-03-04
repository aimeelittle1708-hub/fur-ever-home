from django import forms
from .models import Pet, AdoptionRequest


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


class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us why you would like to adopt this pet and any relevant information about your home...',
                'rows': 5,
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].required = False


class RequestPetForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['pet', 'message']
        widgets = {
            'pet': forms.Select(attrs={
                'class': 'form-select',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': (
                    'Tell us about your home and why you would be '
                    'a great match for this pet...'
                ),
                'rows': 5,
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        available_pets = Pet.objects.filter(
            status=Pet.Status.AVAILABLE,
            authorised=True,
        ).order_by('-featured', '-date_added')

        if user and user.is_authenticated:
            available_pets = available_pets.exclude(user=user)

        self.fields['pet'].queryset = available_pets
        self.fields['pet'].empty_label = 'Choose a pet to request'
        self.fields['message'].required = False
