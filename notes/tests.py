from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models.notes import Note, SharedNote, NoteHistory


class SignupViewTestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user_data = {'username': 'test_user', 'password': 'test_password'}

	def test_signup_success(self):
		response = self.client.post('/signup/', self.user_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_signup_failure(self):
		# Invalid data - missing password
		invalid_data = {'username': 'test_user'}
		response = self.client.post('/signup/', invalid_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateNoteViewTestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create(username='test_user', password='test_password')
		self.client.force_authenticate(user=self.user)
		self.note_data = {'content': 'Test note content'}

	def test_create_note_success(self):
		response = self.client.post('/notes/create/', self.note_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_note_failure(self):
		# Invalid data - missing content
		invalid_data = {}
		response = self.client.post('/notes/create/', invalid_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetOrUpdateNoteViewTestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create(username='test_user', password='test_password')
		self.note = Note.objects.create(owner=self.user, content='Test note content')

	def test_get_note_success(self):
		self.client.force_authenticate(user=self.user)
		response = self.client.get(f'/notes/{self.note.id}/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_note_failure(self):
		# Unauthorized access - user not authenticated
		response = self.client.get(f'/notes/{self.note.id}/')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ShareNoteViewTestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create(username='test_user', password='test_password')
		self.note = Note.objects.create(owner=self.user, content='Test note content')
		self.shared_user = User.objects.create(username='shared_user', password='shared_password')
		self.client.force_authenticate(user=self.user)
		self.share_data = {'note_id': self.note.id, 'user_ids': [self.shared_user.id]}

	def test_share_note_success(self):
		response = self.client.post('/notes/share/', self.share_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_share_note_failure(self):
		# Invalid data - missing note_id
		invalid_data = {'user_ids': [self.shared_user.id]}
		response = self.client.post('/notes/share/', invalid_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NoteVersionHistoryViewTestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create(username='test_user', password='test_password')
		self.note = Note.objects.create(owner=self.user, content='Test note content')

	def test_note_version_history_success(self):
		self.client.force_authenticate(user=self.user)
		response = self.client.get(f'/notes/version-history/{self.note.id}/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_note_version_history_failure(self):
		# Unauthorized access - user not authenticated
		response = self.client.get(f'/notes/version-history/{self.note.id}/')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)