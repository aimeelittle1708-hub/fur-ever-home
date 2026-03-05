from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from .models import Pet, AdoptionRequest, Favourite

User = get_user_model()


class HomeViewTestCase(TestCase):
    """Test cases for home view"""

    def setUp(self):
        self.client = Client()

    def test_home_view_GET(self):
        """Test home view returns 200 and uses correct template"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class ViewPetsTestCase(TestCase):
    """Test cases for view_pets view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.available_pet = Pet.objects.create(
            user=self.user,
            name='Available Dog',
            species=Pet.Species.DOG,
            status=Pet.Status.AVAILABLE,
            authorised=True
        )
        self.unavailable_pet = Pet.objects.create(
            user=self.user,
            name='Unavailable Dog',
            species=Pet.Species.DOG,
            status=Pet.Status.ADOPTED,
            authorised=True
        )
        self.unauthorised_pet = Pet.objects.create(
            user=self.user,
            name='Unauthorised Dog',
            species=Pet.Species.DOG,
            status=Pet.Status.AVAILABLE,
            authorised=False
        )

    def test_view_pets_displays_available_pets(self):
        """Test that only available and authorised pets are displayed"""
        response = self.client.get(reverse('view_pets'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Available Dog')
        self.assertNotContains(response, 'Unavailable Dog')
        self.assertNotContains(response, 'Unauthorised Dog')

    def test_view_pets_species_filter(self):
        """Test filtering pets by species"""
        Pet.objects.create(
            user=self.user,
            name='Test Cat',
            species=Pet.Species.CAT,
            status=Pet.Status.AVAILABLE,
            authorised=True
        )
        response = self.client.get(
            reverse('view_pets'),
            {'species': Pet.Species.CAT}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Cat')
        self.assertNotContains(response, 'Available Dog')


class PetDetailViewTestCase(TestCase):
    """Test cases for pet_detail view"""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username='owner',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.pet = Pet.objects.create(
            user=self.owner,
            name='Test Pet',
            species=Pet.Species.DOG,
            status=Pet.Status.AVAILABLE,
            authorised=True
        )

    def test_pet_detail_owner_can_view_own_pet(self):
        """Test pet owner can view their own pet regardless of status"""
        self.pet.status = Pet.Status.ADOPTED
        self.pet.save()
        self.client.login(username='owner', password='testpass123')
        response = self.client.get(reverse('pet_detail', args=[self.pet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Pet')

    def test_pet_detail_non_owner_can_view_available_pet(self):
        """Test non-owner can view available authorised pets"""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(reverse('pet_detail', args=[self.pet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Pet')

    def test_pet_detail_non_owner_cannot_view_unavailable_pet(self):
        """Test non-owner gets 404 for unavailable pets"""
        self.pet.status = Pet.Status.ADOPTED
        self.pet.save()
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(reverse('pet_detail', args=[self.pet.id]))
        self.assertEqual(response.status_code, 404)

    def test_pet_detail_approved_requester_can_view_adopted_pet(self):
        """Test user with approved request can view adopted pet"""
        self.pet.status = Pet.Status.ADOPTED
        self.pet.save()
        AdoptionRequest.objects.create(
            user=self.other_user,
            pet=self.pet,
            status=AdoptionRequest.Status.APPROVED
        )
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(reverse('pet_detail', args=[self.pet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Pet')


class CreatePetViewTestCase(TestCase):
    """Test cases for create_pet view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='petowner',
            password='testpass123'
        )

    def test_create_pet_requires_login(self):
        """Test that unauthenticated users are redirected"""
        response = self.client.get(reverse('create_pet'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_create_pet_GET(self):
        """Test GET request displays form"""
        self.client.login(username='petowner', password='testpass123')
        response = self.client.get(reverse('create_pet'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_pet.html')

    def test_create_pet_POST_valid_data(self):
        """Test creating pet with valid data"""
        self.client.login(username='petowner', password='testpass123')
        self.client.post(reverse('create_pet'), {
            'name': 'New Pet',
            'species': Pet.Species.DOG,
            'age': 2,
            'gender': Pet.Gender.MALE,
            'description': 'A lovely dog'
        })
        self.assertEqual(Pet.objects.count(), 1)
        pet = Pet.objects.first()
        self.assertEqual(pet.name, 'New Pet')
        self.assertEqual(pet.user, self.user)


class RequestAdoptionViewTestCase(TestCase):
    """Test cases for request_adoption view"""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username='owner',
            password='testpass123'
        )
        self.requester = User.objects.create_user(
            username='requester',
            password='testpass123'
        )
        self.pet = Pet.objects.create(
            user=self.owner,
            name='Adoptable Pet',
            species=Pet.Species.CAT,
            status=Pet.Status.AVAILABLE,
            authorised=True
        )

    def test_request_adoption_requires_login(self):
        """Test that unauthenticated users are redirected"""
        response = self.client.get(
            reverse('request_adoption', args=[self.pet.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_request_adoption_cannot_request_own_pet(self):
        """Test pet owner cannot request their own pet"""
        self.client.login(username='owner', password='testpass123')
        self.client.post(
            reverse('request_adoption', args=[self.pet.id]),
            {'message': 'I want my own pet'}
        )
        self.assertEqual(AdoptionRequest.objects.count(), 0)

    def test_request_adoption_duplicate_request_prevented(self):
        """Test duplicate adoption requests are prevented"""
        AdoptionRequest.objects.create(
            user=self.requester,
            pet=self.pet,
            message='First request'
        )
        self.client.login(username='requester', password='testpass123')
        self.client.post(
            reverse('request_adoption', args=[self.pet.id]),
            {'message': 'Second request'}
        )
        self.assertEqual(AdoptionRequest.objects.count(), 1)

    def test_request_adoption_POST_valid(self):
        """Test successful adoption request creation"""
        self.client.login(username='requester', password='testpass123')
        self.client.post(
            reverse('request_adoption', args=[self.pet.id]),
            {'message': 'I would love to adopt this pet!'}
        )
        self.assertEqual(AdoptionRequest.objects.count(), 1)
        request = AdoptionRequest.objects.first()
        self.assertEqual(request.user, self.requester)
        self.assertEqual(request.pet, self.pet)
        self.assertEqual(request.status, AdoptionRequest.Status.PENDING)


class AcceptAdoptionRequestViewTestCase(TestCase):
    """Test cases for accept_adoption_request view"""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username='owner',
            password='testpass123'
        )
        self.requester = User.objects.create_user(
            username='requester',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.pet = Pet.objects.create(
            user=self.owner,
            name='Pet to Adopt',
            species=Pet.Species.DOG,
            status=Pet.Status.AVAILABLE,
            authorised=True
        )
        self.adoption_request = AdoptionRequest.objects.create(
            user=self.requester,
            pet=self.pet,
            status=AdoptionRequest.Status.PENDING
        )

    def test_accept_request_requires_login(self):
        """Test that unauthenticated users are redirected"""
        response = self.client.get(
            reverse('accept_adoption_request', args=[self.adoption_request.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_accept_request_changes_status_to_approved(self):
        """Test accepting request changes status to APPROVED"""
        self.client.login(username='owner', password='testpass123')
        self.client.get(
            reverse('accept_adoption_request', args=[self.adoption_request.id])
        )
        self.adoption_request.refresh_from_db()
        self.assertEqual(
            self.adoption_request.status,
            AdoptionRequest.Status.APPROVED
        )

    def test_accept_request_changes_pet_status_to_adopted(self):
        """Test accepting request changes pet status to ADOPTED"""
        self.client.login(username='owner', password='testpass123')
        self.client.get(
            reverse('accept_adoption_request', args=[self.adoption_request.id])
        )
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.status, Pet.Status.ADOPTED)

    def test_accept_request_only_by_pet_owner(self):
        """Test only pet owner can accept requests"""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(
            reverse('accept_adoption_request', args=[self.adoption_request.id])
        )
        self.assertEqual(response.status_code, 404)


class RejectAdoptionRequestViewTestCase(TestCase):
    """Test cases for reject_adoption_request view"""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username='owner',
            password='testpass123'
        )
        self.requester = User.objects.create_user(
            username='requester',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.pet = Pet.objects.create(
            user=self.owner,
            name='Pet to Reject',
            species=Pet.Species.CAT,
            status=Pet.Status.AVAILABLE,
            authorised=True
        )
        self.adoption_request = AdoptionRequest.objects.create(
            user=self.requester,
            pet=self.pet,
            status=AdoptionRequest.Status.PENDING
        )

    def test_reject_request_requires_login(self):
        """Test that unauthenticated users are redirected"""
        response = self.client.get(
            reverse('reject_adoption_request', args=[self.adoption_request.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_reject_request_changes_status_to_rejected(self):
        """Test rejecting request changes status to REJECTED"""
        self.client.login(username='owner', password='testpass123')
        self.client.get(
            reverse('reject_adoption_request', args=[self.adoption_request.id])
        )
        self.adoption_request.refresh_from_db()
        self.assertEqual(
            self.adoption_request.status,
            AdoptionRequest.Status.REJECTED
        )

    def test_reject_request_only_by_pet_owner(self):
        """Test only pet owner can reject requests"""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(
            reverse('reject_adoption_request', args=[self.adoption_request.id])
        )
        self.assertEqual(response.status_code, 404)


class SavePetViewTestCase(TestCase):
    """Test cases for save_pet view"""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username='owner',
            password='testpass123'
        )
        self.user = User.objects.create_user(
            username='user',
            password='testpass123'
        )
        self.pet = Pet.objects.create(
            user=self.owner,
            name='Pet to Save',
            species=Pet.Species.DOG,
            status=Pet.Status.AVAILABLE,
            authorised=True
        )

    def test_save_pet_requires_login(self):
        """Test that unauthenticated users are redirected"""
        response = self.client.get(reverse('save_pet', args=[self.pet.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_save_pet_cannot_save_own_pet(self):
        """Test pet owner cannot save their own pet"""
        self.client.login(username='owner', password='testpass123')
        self.client.post(reverse('save_pet', args=[self.pet.id]))
        self.assertEqual(Favourite.objects.count(), 0)

    def test_save_pet_duplicate_prevented(self):
        """Test duplicate favourites are handled correctly"""
        Favourite.objects.create(user=self.user, pet=self.pet)
        self.client.login(username='user', password='testpass123')
        self.client.post(reverse('save_pet', args=[self.pet.id]))
        self.assertEqual(Favourite.objects.count(), 1)

    def test_save_pet_creates_favourite(self):
        """Test successfully saving a pet to favourites"""
        self.client.login(username='user', password='testpass123')
        self.client.post(reverse('save_pet', args=[self.pet.id]))
        self.assertEqual(Favourite.objects.count(), 1)
        favourite = Favourite.objects.first()
        self.assertEqual(favourite.user, self.user)
        self.assertEqual(favourite.pet, self.pet)
