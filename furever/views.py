from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Pet
from .forms import PetForm


def home(request):
    return render(request, 'home.html')


def view_pets(request):
    pets = Pet.objects.filter(
        status=Pet.Status.AVAILABLE,
        authorised=True,
    ).order_by('-featured', '-date_added')
    return render(request, 'view_pets.html', {'pets': pets})


def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id, status=Pet.Status.AVAILABLE)
    
    # Allow owners to see their own pets even if not authorised
    is_owner = request.user.is_authenticated and pet.user == request.user
    if not pet.authorised and not is_owner:
        # Non-owners can't see unauthorised pets
        from django.http import Http404
        raise Http404("No Pet matches the given query.")
    
    return render(request, 'pet_detail.html', {'pet': pet})


@login_required
def create_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.user = request.user
            pet.save()
            return redirect('pet_detail', pet_id=pet.id)
    else:
        form = PetForm()
    return render(request, 'create_pet.html', {'form': form})


def request_pets(request):
    return render(request, 'request_pets.html')


def success_stories(request):
    return render(request, 'success_stories.html')


def about(request):
    return render(request, 'about.html')
