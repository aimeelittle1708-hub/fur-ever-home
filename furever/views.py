from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db import IntegrityError
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Pet, AdoptionRequest, Favourite, Comment
from .forms import (
    PetForm,
    AdoptionRequestForm,
    RequestPetForm,
    FavouriteForm,
    CommentForm,
)


def home(request):
    from .models import Pet
    featured_pets = Pet.objects.filter(featured=True, authorised=True, status=Pet.Status.AVAILABLE).order_by('-date_added')[:3]
    return render(request, 'home.html', {'featured_pets': featured_pets})


def view_pets(request):
    pets = Pet.objects.filter(
        status=Pet.Status.AVAILABLE,
        authorised=True,
    ).order_by('-featured', '-date_added')
    return render(request, 'view_pets.html', {'pets': pets})


def request_pet_start(request):
    target_url = reverse('request_pet_form')
    if request.user.is_authenticated:
        return redirect(target_url)

    login_url = reverse('account_login')
    return redirect(f'{login_url}?next={target_url}')


@login_required
@ensure_csrf_cookie
def request_pet_form(request):
    if request.method == 'POST':
        form = RequestPetForm(request.POST, user=request.user)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.user = request.user

            try:
                adoption_request.save()
            except IntegrityError:
                messages.warning(
                    request,
                    'You already submitted a request for this pet.',
                )
                return redirect('pet_detail', pet_id=adoption_request.pet.id)

            messages.success(
                request,
                'Your adoption request was submitted successfully!',
            )
            return redirect('request_pets')
    else:
        form = RequestPetForm(user=request.user)

    if not form.fields['pet'].queryset.exists():
        messages.info(request, 'No pets are currently available to request.')
        return redirect('view_pets')

    return render(request, 'request_pet_form.html', {'form': form})


def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id, status=Pet.Status.AVAILABLE)
    
    # Allow owners to see their own pets even if not authorised
    is_owner = request.user.is_authenticated and pet.user == request.user
    if not pet.authorised and not is_owner:
        # Non-owners can't see unauthorised pets
        from django.http import Http404
        raise Http404("No Pet matches the given query.")
    
    # Check if user has already requested this pet
    has_requested = False
    saved_pet = None
    if request.user.is_authenticated:
        has_requested = AdoptionRequest.objects.filter(
            user=request.user,
            pet=pet
        ).exists()
        saved_pet = Favourite.objects.filter(
            user=request.user,
            pet=pet,
        ).first()

    comments = Comment.objects.filter(pet=pet).select_related('user')
    
    return render(request, 'pet_detail.html', {
        'pet': pet,
        'has_requested': has_requested,
        'is_owner': is_owner,
        'saved_pet': saved_pet,
        'comments': comments,
        'comment_form': CommentForm(),
    })


@login_required
def save_pet(request, pet_id):
    pet = get_object_or_404(
        Pet,
        pk=pet_id,
        status=Pet.Status.AVAILABLE,
        authorised=True,
    )

    if pet.user == request.user:
        messages.error(request, 'You cannot save your own pet listing.')
        return redirect('pet_detail', pet_id=pet.id)

    favourite = Favourite.objects.filter(user=request.user, pet=pet).first()
    form = FavouriteForm(request.POST or None)

    if favourite:
        if request.method == 'POST' and form.is_valid():
            favourite.notes = form.cleaned_data.get('notes', '')
            favourite.save()
            messages.success(request, f'Updated saved notes for {pet.name}.')
        else:
            messages.info(request, f'{pet.name} is already in your saved pets.')
        return redirect('pet_detail', pet_id=pet.id)

    new_favourite = Favourite(user=request.user, pet=pet)
    if request.method == 'POST' and form.is_valid():
        new_favourite.notes = form.cleaned_data.get('notes', '')
    new_favourite.save()
    messages.success(request, f'{pet.name} has been saved to your list.')
    return redirect('pet_detail', pet_id=pet.id)


@login_required
def saved_pets(request):
    favourites = Favourite.objects.filter(user=request.user).select_related(
        'pet'
    ).order_by('-save_date')
    return render(request, 'saved_pets.html', {'favourites': favourites})


@login_required
def edit_saved_pet(request, favourite_id):
    favourite = get_object_or_404(Favourite, pk=favourite_id, user=request.user)

    if request.method == 'POST':
        form = FavouriteForm(request.POST, instance=favourite)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saved pet note updated.')
            return redirect('saved_pets')
    else:
        form = FavouriteForm(instance=favourite)

    return render(
        request,
        'edit_saved_pet.html',
        {'form': form, 'favourite': favourite},
    )


@login_required
def delete_saved_pet(request, favourite_id):
    favourite = get_object_or_404(Favourite, pk=favourite_id, user=request.user)

    if request.method == 'POST':
        pet_name = favourite.pet.name
        favourite.delete()
        messages.success(request, f'{pet_name} removed from saved pets.')
        return redirect('saved_pets')

    return render(
        request,
        'delete_saved_pet.html',
        {'favourite': favourite},
    )


@login_required
def add_comment(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id, status=Pet.Status.AVAILABLE)

    is_owner = pet.user == request.user
    if not pet.authorised and not is_owner:
        from django.http import Http404
        raise Http404('No Pet matches the given query.')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.pet = pet
            comment.save()
            messages.success(request, 'Comment added successfully.')

    return redirect('pet_detail', pet_id=pet.id)


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, user=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully.')
            return redirect('pet_detail', pet_id=comment.pet.id)
    else:
        form = CommentForm(instance=comment)

    return render(
        request,
        'edit_comment.html',
        {'form': form, 'comment': comment},
    )


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, user=request.user)

    if request.method == 'POST':
        pet_id = comment.pet.id
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
        return redirect('pet_detail', pet_id=pet_id)

    return render(
        request,
        'delete_comment.html',
        {'comment': comment},
    )


@login_required
def create_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.user = request.user
            pet.save()
            messages.success(
                request,
                (
                    'Pet listing created successfully! It will be visible '
                    'once approved by an admin.'
                ),
            )
            return redirect('pet_detail', pet_id=pet.id)
    else:
        form = PetForm()
    return render(request, 'create_pet.html', {'form': form})


@login_required
def my_pets(request):
    pets = Pet.objects.filter(user=request.user).order_by('-date_added')
    return render(request, 'my_pets.html', {'pets': pets})


@login_required
def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id, user=request.user)

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            updated_pet = form.save(commit=False)
            updated_pet.authorised = False
            updated_pet.save()
            messages.success(
                request,
                (
                    'Pet updated successfully. It is now pending '
                    'admin re-approval.'
                ),
            )
            return redirect('pet_detail', pet_id=pet.id)
    else:
        form = PetForm(instance=pet)

    return render(
        request,
        'edit_pet.html',
        {'form': form, 'pet': pet},
    )


@login_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id, user=request.user)

    if request.method == 'POST':
        pet_name = pet.name
        pet.delete()
        messages.success(request, f'{pet_name} was deleted successfully.')
        return redirect('my_pets')

    return render(request, 'delete_pet.html', {'pet': pet})


@login_required
@ensure_csrf_cookie
def request_adoption(request, pet_id):
    pet = get_object_or_404(
        Pet,
        pk=pet_id,
        status=Pet.Status.AVAILABLE,
        authorised=True,
    )
    
    # Check if user is trying to adopt their own pet
    if pet.user == request.user:
        messages.error(request, 'You cannot request to adopt your own pet.')
        return redirect('pet_detail', pet_id=pet.id)
    
    # Check if user has already requested this pet
    if AdoptionRequest.objects.filter(user=request.user, pet=pet).exists():
        messages.warning(
            request,
            'You have already submitted an adoption request for this pet.',
        )
        return redirect('pet_detail', pet_id=pet.id)
    
    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.user = request.user
            adoption_request.pet = pet
            adoption_request.save()
            messages.success(
                request,
                (
                    f'Your adoption request for {pet.name} has '
                    'been submitted successfully!'
                ),
            )
            return redirect('request_pets')
    else:
        form = AdoptionRequestForm()
    
    return render(request, 'request_adoption.html', {'form': form, 'pet': pet})


@login_required
def request_pets(request):
    # Show user's adoption requests
    adoption_requests = AdoptionRequest.objects.filter(
        user=request.user
    ).select_related('pet').order_by('-request_date')
    
    return render(
        request,
        'request_pets.html',
        {'adoption_requests': adoption_requests},
    )


@login_required
def edit_request(request, request_id):
    adoption_request = get_object_or_404(
        AdoptionRequest,
        pk=request_id,
        user=request.user,
    )

    if adoption_request.status != AdoptionRequest.Status.PENDING:
        messages.error(request, 'Only pending requests can be edited.')
        return redirect('request_pets')

    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST, instance=adoption_request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Adoption request updated successfully.')
            return redirect('request_pets')
    else:
        form = AdoptionRequestForm(instance=adoption_request)

    return render(
        request,
        'edit_request.html',
        {'form': form, 'adoption_request': adoption_request},
    )


@login_required
def delete_request(request, request_id):
    adoption_request = get_object_or_404(
        AdoptionRequest,
        pk=request_id,
        user=request.user,
    )

    if request.method == 'POST':
        pet_name = adoption_request.pet.name
        adoption_request.delete()
        messages.success(request, f'Request for {pet_name} deleted.')
        return redirect('request_pets')

    return render(
        request,
        'delete_request.html',
        {'adoption_request': adoption_request},
    )


@login_required
def cancel_request(request, request_id):
    adoption_request = get_object_or_404(
        AdoptionRequest,
        pk=request_id,
        user=request.user
    )
    
    if request.method == 'POST':
        pet_name = adoption_request.pet.name
        adoption_request.status = AdoptionRequest.Status.CANCELLED
        adoption_request.save()
        messages.success(
            request,
            f'Your adoption request for {pet_name} has been cancelled.',
        )
        return redirect('request_pets')
    
    return render(
        request,
        'cancel_request.html',
        {'adoption_request': adoption_request},
    )


def success_stories(request):
    return render(request, 'success_stories.html')


def about(request):
    return render(request, 'about.html')
