from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(title="Заголовок",
                                       text="Текст",
                                       author = cls.author)

    def test_note_in_object_list(self):
        self.client.force_login(self.author)
        url = reverse('notes:list')
        response = self.client.get(url)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_note_list_for_different_users(self):
        users_statuses = (
                (self.author, True),
                (self.reader, False),
            )
        for user, status in users_statuses:
            self.client.force_login(user)
            with self.subTest(user=user, status=status):
                url = reverse('notes:list')
                response = self.client.get(url)
                object_list = response.context['object_list']
                self.assertEqual(self.note in object_list, status)

    def test_pages_contains_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
            )
        self.client.force_login(self.author)
        for name, args in urls:
            with self.subTest():
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)