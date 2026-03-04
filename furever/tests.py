from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Comment, Favourite, Pet


class SaveAndCommentCrudTests(TestCase):
	def setUp(self):
		self.user_model = get_user_model()
		self.owner = self.user_model.objects.create_user(
			username='owner_user',
			password='pass12345',
		)
		self.adopter = self.user_model.objects.create_user(
			username='adopter_user',
			password='pass12345',
		)
		self.pet = Pet.objects.create(
			user=self.owner,
			name='Test Pet',
			species=Pet.Species.DOG,
			age=3,
			gender=Pet.Gender.UNKNOWN,
			status=Pet.Status.AVAILABLE,
			authorised=True,
		)
		self.client.login(username='adopter_user', password='pass12345')

	def test_saved_pet_full_crud(self):
		save_response = self.client.post(
			reverse('save_pet', args=[self.pet.id]),
			{'notes': 'first note'},
			follow=True,
		)
		self.assertEqual(save_response.status_code, 200)

		favourite = Favourite.objects.get(user=self.adopter, pet=self.pet)
		self.assertEqual(favourite.notes, 'first note')

		edit_response = self.client.post(
			reverse('edit_saved_pet', args=[favourite.id]),
			{'notes': 'updated note'},
			follow=True,
		)
		self.assertEqual(edit_response.status_code, 200)
		favourite.refresh_from_db()
		self.assertEqual(favourite.notes, 'updated note')

		delete_response = self.client.post(
			reverse('delete_saved_pet', args=[favourite.id]),
			follow=True,
		)
		self.assertEqual(delete_response.status_code, 200)
		self.assertFalse(Favourite.objects.filter(id=favourite.id).exists())

	def test_comment_full_crud(self):
		add_response = self.client.post(
			reverse('add_comment', args=[self.pet.id]),
			{'content': 'first comment'},
			follow=True,
		)
		self.assertEqual(add_response.status_code, 200)

		comment = Comment.objects.get(user=self.adopter, pet=self.pet)
		self.assertEqual(comment.content, 'first comment')

		edit_response = self.client.post(
			reverse('edit_comment', args=[comment.id]),
			{'content': 'updated comment'},
			follow=True,
		)
		self.assertEqual(edit_response.status_code, 200)
		comment.refresh_from_db()
		self.assertEqual(comment.content, 'updated comment')

		delete_response = self.client.post(
			reverse('delete_comment', args=[comment.id]),
			follow=True,
		)
		self.assertEqual(delete_response.status_code, 200)
		self.assertFalse(Comment.objects.filter(id=comment.id).exists())
