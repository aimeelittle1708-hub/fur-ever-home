from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pets/', views.view_pets, name='view_pets'),
    path('pets/mine/', views.my_pets, name='my_pets'),
    path('pets/saved/', views.saved_pets, name='saved_pets'),
    path('request-a-pet/', views.request_pet_start, name='request_pet_start'),
    # path('requests/new/', views.request_pet_form, name='request_pet_form'),
    path('pets/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('pets/create/', views.create_pet, name='create_pet'),
    path('pets/<int:pet_id>/edit/', views.edit_pet, name='edit_pet'),
    path('pets/<int:pet_id>/delete/', views.delete_pet, name='delete_pet'),
    path('pets/<int:pet_id>/save/', views.save_pet, name='save_pet'),
    path(
        'saved-pets/<int:favourite_id>/edit/',
        views.edit_saved_pet,
        name='edit_saved_pet',
    ),
    path(
        'saved-pets/<int:favourite_id>/delete/',
        views.delete_saved_pet,
        name='delete_saved_pet',
    ),
    path('pets/<int:pet_id>/comments/add/', views.add_comment, name='add_comment'),
    path(
        'comments/<int:comment_id>/edit/',
        views.edit_comment,
        name='edit_comment',
    ),
    path(
        'comments/<int:comment_id>/delete/',
        views.delete_comment,
        name='delete_comment',
    ),
    path(
        'pets/<int:pet_id>/request/',
        views.request_adoption,
        name='request_adoption',
    ),
    path('requests/', views.request_pets, name='request_pets'),
    path(
        'requests/<int:request_id>/edit/',
        views.edit_request,
        name='edit_request',
    ),
    path(
        'requests/<int:request_id>/delete/',
        views.delete_request,
        name='delete_request',
    ),
    path(
        'requests/<int:request_id>/cancel/',
        views.cancel_request,
        name='cancel_request',
    ),
    path('success-stories/', views.success_stories, name='success_stories'),
]
