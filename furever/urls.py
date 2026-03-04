from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pets/', views.view_pets, name='view_pets'),
    path('pets/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('pets/create/', views.create_pet, name='create_pet'),
    path('pets/request/', views.request_pets, name='request_pets'),
]
