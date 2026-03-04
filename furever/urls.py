from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pets/', views.view_pets, name='view_pets'),
    path('request-a-pet/', views.request_pet_start, name='request_pet_start'),
    path('requests/new/', views.request_pet_form, name='request_pet_form'),
    path('pets/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('pets/create/', views.create_pet, name='create_pet'),
    path('pets/<int:pet_id>/request/', views.request_adoption, name='request_adoption'),
    path('requests/', views.request_pets, name='request_pets'),
    path('requests/<int:request_id>/cancel/', views.cancel_request, name='cancel_request'),
    path('success-stories/', views.success_stories, name='success_stories'),
    path('about/', views.about, name='about'),
]
