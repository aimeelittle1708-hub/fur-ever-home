from django.shortcuts import get_object_or_404, render
from .models import Pet


def home(request):
    return render(request, 'home.html')


def view_pets(request):
    pets = Pet.objects.filter(
        status=Pet.Status.AVAILABLE,
        authorised=True,
    ).order_by('-featured', '-date_added')
    return render(request, 'view_pets.html', {'pets': pets})


def pet_detail(request, pet_id):
    pet = get_object_or_404(
        Pet,
        pk=pet_id,
        status=Pet.Status.AVAILABLE,
        authorised=True,
    )
    return render(request, 'pet_detail.html', {'pet': pet})


def request_pets(request):
    return render(request, 'request_pets.html')


def success_stories(request):
    return render(request, 'success_stories.html')


def about(request):
    return render(request, 'about.html')
