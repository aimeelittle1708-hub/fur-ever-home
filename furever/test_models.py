from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db import IntegrityError
from .models import Pet, UserProfile, AdoptionRequest, Favourite, Comment

User = get_user_model()


class UserProfileTestCase(TestCase):
    """Test cases for UserProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )

    def test_user_profile_creation(self):
        """Test creating a UserProfile"""
        profile = UserProfile.objects.create(
            user=self.user,
            phone='555-1234',
            address='123 Test St'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.phone, '555-1234')
        self.assertEqual(profile.address, '123 Test St')

    def test_user_profile_one_to_one_relationship(self):
        """Test OneToOne relationship with User"""
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(self.user.profile, profile)
        self.assertEqual(profile.user, self.user)


class PetTestCase(TestCase):
    """Test cases for Pet model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='petowner',
            email='owner@example.com',
            password='testpass123'
        )

    def test_pet_creation(self):
        """Test creating a Pet"""
        pet = Pet.objects.create(
            user=self.user,
            name='Fluffy',
            species=Pet.Species.CAT,
            breed='Persian',
            age=3
        )
        self.assertEqual(pet.name, 'Fluffy')
        self.assertEqual(pet.species, Pet.Species.CAT)
        self.assertEqual(pet.breed, 'Persian')
        self.assertEqual(pet.age, 3)
        self.assertEqual(pet.user, self.user)

    def test_pet_string_representation(self):
        """Test __str__ method of Pet"""
        pet = Pet.objects.create(
            user=self.user,
            name='Max',
            species=Pet.Species.DOG
        )
        self.assertEqual(str(pet), 'Max (Dog)')

    def test_pet_default_status(self):
        """Test default status is AVAILABLE"""
        pet = Pet.objects.create(
            user=self.user,
            name='Buddy',
            species=Pet.Species.DOG
        )
        self.assertEqual(pet.status, Pet.Status.AVAILABLE)

    def test_pet_user_foreign_key(self):
        """Test ForeignKey relationship with User"""
        pet = Pet.objects.create(
            user=self.user,
            name='Whiskers',
            species=Pet.Species.CAT
        )
        self.assertEqual(pet.user, self.user)
        self.assertIn(pet, self.user.pets.all())


class AdoptionRequestTestCase(TestCase):
    """Test cases for AdoptionRequest model"""

    def setUp(self):
        self.pet_owner = User.objects.create_user(
            username='petowner',
            email='owner@example.com',
            password='testpass123'
        )
        self.requester = User.objects.create_user(
            username='requester',
            email='requester@example.com',
            password='testpass123'
        )
        self.pet = Pet.objects.create(
            user=self.pet_owner,
            name='Buddy',
            species=Pet.Species.DOG
        )

    def test_adoption_request_creation(self):
        """Test creating an AdoptionRequest"""
        request = AdoptionRequest.objects.create(
            user=self.requester,
            pet=self.pet,
            message='I would love to adopt Buddy!'
        )
        self.assertEqual(request.user, self.requester)
        self.assertEqual(request.pet, self.pet)
        self.assertEqual(request.message, 'I would love to adopt Buddy!')

    def test_adoption_request_default_status(self):
        """Test default status is PENDING"""
        request = AdoptionRequest.objects.create(
            user=self.requester,
            pet=self.pet
        )
        self.assertEqual(request.status, AdoptionRequest.Status.PENDING)

    def test_adoption_request_unique_together_constraint(self):
        """Test that user and pet combination must be unique"""
        AdoptionRequest.objects.create(user=self.requester, pet=self.pet)
        with self.assertRaises(IntegrityError):
            AdoptionRequest.objects.create(user=self.requester, pet=self.pet)

    def test_adoption_request_duplicate_raises_error(self):
        """Test that duplicate requests raise IntegrityError"""
        AdoptionRequest.objects.create(user=self.requester, pet=self.pet)
        with self.assertRaises(IntegrityError):
            AdoptionRequest.objects.create(user=self.requester, pet=self.pet)


class FavouriteTestCase(TestCase):
    """Test cases for Favourite model"""

    def setUp(self):
        self.pet_owner = User.objects.create_user(
            username='petowner',
            email='owner@example.com',
            password='testpass123'
        )
        self.user = User.objects.create_user(
            username='favuser',
            email='fav@example.com',
            password='testpass123'
        )
        self.pet = Pet.objects.create(
            user=self.pet_owner,
            name='Luna',
            species=Pet.Species.CAT
        )

    def test_favourite_creation(self):
        """Test creating a Favourite"""
        favourite = Favourite.objects.create(
            user=self.user,
            pet=self.pet,
            notes='Cute and friendly!'
        )
        self.assertEqual(favourite.user, self.user)
        self.assertEqual(favourite.pet, self.pet)
        self.assertEqual(favourite.notes, 'Cute and friendly!')

    def test_favourite_unique_together_constraint(self):
        """Test that user and pet combination must be unique"""
        Favourite.objects.create(user=self.user, pet=self.pet)
        with self.assertRaises(IntegrityError):
            Favourite.objects.create(user=self.user, pet=self.pet)

    def test_favourite_duplicate_raises_error(self):
        """Test that duplicate favourites raise IntegrityError"""
        Favourite.objects.create(user=self.user, pet=self.pet)
        with self.assertRaises(IntegrityError):
            Favourite.objects.create(user=self.user, pet=self.pet)


class CommentTestCase(TestCase):
    """Test cases for Comment model"""

    def setUp(self):
        self.pet_owner = User.objects.create_user(
            username='petowner',
            email='owner@example.com',
            password='testpass123'
        )
        self.commenter = User.objects.create_user(
            username='commenter',
            email='commenter@example.com',
            password='testpass123'
        )
        self.pet = Pet.objects.create(
            user=self.pet_owner,
            name='Rex',
            species=Pet.Species.DOG
        )

    def test_comment_creation(self):
        """Test creating a Comment"""
        comment = Comment.objects.create(
            user=self.commenter,
            pet=self.pet,
            content='What a beautiful dog!'
        )
        self.assertEqual(comment.user, self.commenter)
        self.assertEqual(comment.pet, self.pet)
        self.assertEqual(comment.content, 'What a beautiful dog!')

    def test_comment_string_representation(self):
        """Test __str__ method of Comment"""
        comment = Comment.objects.create(
            user=self.commenter,
            pet=self.pet,
            content='Great pet!'
        )
        self.assertEqual(str(comment), f'Comment by {self.commenter} on {self.pet}')

    def test_comment_pet_foreign_key(self):
        """Test ForeignKey relationship with Pet"""
        comment = Comment.objects.create(
            user=self.commenter,
            pet=self.pet,
            content='Lovely!'
        )
        self.assertEqual(comment.pet, self.pet)
        self.assertIn(comment, self.pet.comments.all())

