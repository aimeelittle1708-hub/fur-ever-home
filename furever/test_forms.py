from django.contrib.auth import get_user_model
from django.test import TestCase

from .forms import (
    AdoptionRequestForm,
    CommentForm,
    FavouriteForm,
    PetForm,
    RequestPetForm,
)
from .models import Comment, Favourite, Pet


class BaseFormTestCase(TestCase):
    """Shared setup and helpers for form tests."""

    def setUp(self):
        self.user_model = get_user_model()
        self._requester = None
        self._owner = None
        self._available_pet = None

    @property
    def requester(self):
        if self._requester is None:
            self._requester = self.user_model.objects.create_user(
                username='requester_user',
                password='pass12345',
            )
        return self._requester

    @property
    def owner(self):
        if self._owner is None:
            self._owner = self.user_model.objects.create_user(
                username='pet_owner',
                password='pass12345',
            )
        return self._owner

    @property
    def available_pet(self):
        if self._available_pet is None:
            self._available_pet = self.make_pet(
                name='Lucky',
                user=self.owner,
                status=Pet.Status.AVAILABLE,
                authorised=True,
            )
        return self._available_pet

    def make_pet(self, **overrides):
        data = {
            'user': self.owner,
            'name': 'Default Pet',
            'species': Pet.Species.DOG,
            'age': 2,
            'gender': Pet.Gender.MALE,
            'status': Pet.Status.AVAILABLE,
            'authorised': True,
        }
        data.update(overrides)
        return Pet.objects.create(**data)

    def valid_pet_data(self, **overrides):
        data = {
            'name': 'Fluffy',
            'species': Pet.Species.DOG,
            'age': 2,
            'gender': Pet.Gender.MALE,
        }
        data.update(overrides)
        return data

    def valid_request_pet_data(self, **overrides):
        data = {
            'pet': self.available_pet.id,
            'message': 'I can provide a loving home.',
        }
        data.update(overrides)
        return data


class PetFormTestCase(BaseFormTestCase):
    """Tests for PetForm"""

    def test_valid_pet_form(self):
        """Test PetForm with valid data"""
        form = PetForm(data=self.valid_pet_data())
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_invalid_pet_form(self):
        """Test PetForm with invalid data"""
        data = {
            'name': '',
            'species': '',
            'age': -1,
            'gender': '',
        }
        form = PetForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertGreater(len(form.errors), 0)

    def test_pet_form_optional_fields(self):
        """Test that optional fields work correctly in PetForm"""
        form = PetForm(
            data=self.valid_pet_data(
                name='Whiskers',
                species=Pet.Species.CAT,
                age=3,
                gender=Pet.Gender.FEMALE,
            )
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_pet_form_save(self):
        """Test PetForm save functionality"""
        form = PetForm(data=self.valid_pet_data(name='Buddy', age=4))
        self.assertTrue(form.is_valid())

        pet = form.save(commit=False)
        pet.user = self.owner
        pet.save()

        self.assertEqual(pet.name, 'Buddy')
        self.assertEqual(pet.species, Pet.Species.DOG)
        self.assertEqual(pet.age, 4)
        self.assertEqual(pet.gender, Pet.Gender.MALE)


class AdoptionRequestFormTestCase(BaseFormTestCase):
    """Tests for AdoptionRequestForm"""

    def test_valid_adoption_request_form(self):
        """Test AdoptionRequestForm with valid data"""
        data = {
            'message': 'I would love to adopt this pet!',
        }
        form = AdoptionRequestForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_invalid_adoption_request_form(self):
        """Test AdoptionRequestForm with invalid data"""
        form = AdoptionRequestForm(data=None)
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_adoption_request_message_optional(self):
        """Test that message field is optional in AdoptionRequestForm"""
        data = {
            'message': '',
        }
        form = AdoptionRequestForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_adoption_request_form_save(self):
        """Test AdoptionRequestForm save functionality"""
        data = {
            'message': 'I would love to adopt this pet!',
        }
        form = AdoptionRequestForm(data=data)
        self.assertTrue(form.is_valid())

        adoption_request = form.save(commit=False)
        adoption_request.user = self.requester
        adoption_request.pet = self.available_pet
        adoption_request.save()

        self.assertEqual(
            adoption_request.message,
            'I would love to adopt this pet!',
        )
        self.assertEqual(adoption_request.user, self.requester)
        self.assertEqual(adoption_request.pet, self.available_pet)


class RequestPetFormTestCase(BaseFormTestCase):
    """Tests for RequestPetForm"""

    def test_valid_request_pet_form(self):
        """Test RequestPetForm with valid data"""
        form = RequestPetForm(
            data=self.valid_request_pet_data(),
            user=self.requester,
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_invalid_request_pet_form(self):
        """Test RequestPetForm with invalid data"""
        data = {
            'message': 'I can provide a loving home.',
        }
        form = RequestPetForm(data=data, user=self.requester)
        self.assertFalse(form.is_valid())
        self.assertIn('pet', form.errors)

    def test_request_pet_form_excludes_user_pets(self):
        """Test that RequestPetForm excludes pets owned by the current user"""
        own_pet = self.make_pet(
            user=self.requester,
            name='Requester Pet',
            status=Pet.Status.AVAILABLE,
            authorised=True,
        )

        form = RequestPetForm(user=self.requester)
        queryset = form.fields['pet'].queryset

        self.assertIn(self.available_pet, queryset)
        self.assertNotIn(own_pet, queryset)

    def test_request_pet_form_only_available_pets(self):
        """Test that RequestPetForm only shows available and authorised pets"""
        pending_pet = self.make_pet(
            name='Pending Pet',
            status=Pet.Status.PENDING,
            authorised=True,
        )
        unauthorised_pet = self.make_pet(
            name='Unauthorised Pet',
            status=Pet.Status.AVAILABLE,
            authorised=False,
        )

        form = RequestPetForm(user=self.requester)
        queryset = form.fields['pet'].queryset

        self.assertIn(self.available_pet, queryset)
        self.assertNotIn(pending_pet, queryset)
        self.assertNotIn(unauthorised_pet, queryset)

    def test_request_pet_form_message_optional(self):
        """Test that message field is optional in RequestPetForm"""
        data = self.valid_request_pet_data(message='')
        form = RequestPetForm(data=data, user=self.requester)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_request_pet_form_save(self):
        """Test RequestPetForm save functionality"""
        form = RequestPetForm(
            data=self.valid_request_pet_data(),
            user=self.requester,
        )
        self.assertTrue(form.is_valid())

        adoption_request = form.save(commit=False)
        adoption_request.user = self.requester
        adoption_request.save()

        self.assertEqual(adoption_request.user, self.requester)
        self.assertEqual(adoption_request.pet, self.available_pet)
        self.assertEqual(
            adoption_request.message,
            'I can provide a loving home.',
        )
        self.assertEqual(
            adoption_request.status,
            adoption_request.Status.PENDING,
        )


class FavouriteFormTestCase(BaseFormTestCase):
    """Tests for FavouriteForm"""

    def test_valid_favourite_form(self):
        """Test FavouriteForm with valid data"""
        data = {
            'notes': 'Great with kids',
        }
        form = FavouriteForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_invalid_favourite_form(self):
        """Test FavouriteForm with invalid data"""
        form = FavouriteForm(data=None)
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_favourite_form_notes_optional(self):
        """Test that notes field is optional in FavouriteForm"""
        data = {
            'notes': '',
        }
        form = FavouriteForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_favourite_form_save(self):
        """Test FavouriteForm save functionality"""
        data = {
            'notes': 'Save this pet',
        }
        form = FavouriteForm(data=data)
        self.assertTrue(form.is_valid())

        favourite = form.save(commit=False)
        favourite.user = self.requester
        favourite.pet = self.available_pet
        favourite.save()

        self.assertEqual(favourite.user, self.requester)
        self.assertEqual(favourite.pet, self.available_pet)
        self.assertEqual(favourite.notes, 'Save this pet')
        self.assertIsInstance(favourite, Favourite)


class CommentFormTestCase(BaseFormTestCase):
    """Tests for CommentForm"""

    def test_valid_comment_form(self):
        """Test CommentForm with valid data"""
        data = {
            'content': 'Lovely pet profile.',
        }
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_invalid_comment_form(self):
        """Test CommentForm with invalid data"""
        data = {
            'content': '',
        }
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_comment_form_save(self):
        """Test CommentForm save functionality"""
        data = {
            'content': 'I would love to adopt this pet!',
        }
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

        comment = form.save(commit=False)
        comment.user = self.requester
        comment.pet = self.available_pet
        comment.save()

        self.assertEqual(comment.user, self.requester)
        self.assertEqual(comment.pet, self.available_pet)
        self.assertEqual(comment.content, 'I would love to adopt this pet!')
        self.assertIsInstance(comment, Comment)
