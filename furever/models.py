from django.conf import settings
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extends Django's built-in user with the extra fields shown in your ERD.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Profile: {self.user}"


class Pet(models.Model):
    class Species(models.IntegerChoices):
        DOG = 1, "Dog"
        CAT = 2, "Cat"
        FISH = 3, "Fish"
        REPITLE = 4, "Reptile"
        BIRD = 5, "Bird"
        FUNGI = 6, "Fungi"
        MOLLUSC = 7, "Mollusc"
        INSECT = 8, "Insect"
        OTHER = 9, "Other"

    class Gender(models.IntegerChoices):
        MALE = 1, "Male"
        FEMALE = 2, "Female"
        UNKNOWN = 3, "Unknown"

    class Status(models.IntegerChoices):
        AVAILABLE = 1, "Available"
        PENDING = 2, "Pending"
        ADOPTED = 3, "Adopted"
        INACTIVE = 4, "Inactive"

    # FK to User_ID in your ERD (the owner/poster of the pet)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pets",
    )

    name = models.CharField(max_length=120)
    species = models.IntegerField(choices=Species.choices)
    breed = models.CharField(max_length=120, blank=True)
    age = models.PositiveIntegerField(default=0)
    gender = models.IntegerField(choices=Gender.choices, default=Gender.UNKNOWN)

    description = models.TextField(blank=True)

    date_added = models.DateTimeField(auto_now_add=True)

    # Photo in ERD: cloudinary; fallback to ImageField if cloudinary not installed
    if CloudinaryField:
        photo = CloudinaryField("image", blank=True, null=True)
    else:
        photo = models.ImageField(upload_to="pets/", blank=True, null=True)

    location = models.CharField(max_length=255, blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.AVAILABLE)

    authorised = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.get_species_display()})"


class AdoptionRequest(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1, "Pending"
        APPROVED = 2, "Approved"
        REJECTED = 3, "Rejected"
        CANCELLED = 4, "Cancelled"

    # FK User_ID (requester)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="adoption_requests",
    )
    # FK Pet_ID
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name="adoption_requests",
    )

    request_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    message = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "pet"]),
            models.Index(fields=["status"]),
        ]
        # Prevent the same user from requesting the same pet multiple times
        unique_together = ("user", "pet")

    def __str__(self) -> str:
        return f"Request #{self.pk}: {self.user} -> {self.pet}"


class Favourite(models.Model):
    # FK User_ID
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favourites",
    )
    # FK Pet_ID
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name="favourited_by",
    )

    save_date = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("user", "pet")
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["pet"]),
        ]

    def __str__(self) -> str:
        return f"{self.user} ♥ {self.pet}"