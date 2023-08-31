from django.test import TestCase, RequestFactory
from django.contrib.messages import get_messages
from django.urls import reverse
from books.views import add_book_view


class AddBookViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_add_book_view_post_success(self):
        url = reverse('book_routes:add_book_view')
        data = {
            'title': 'Test Title',
            'author': 'Test Author',
            'isbn': '1234567890',
            'cover_image': 'test_cover_image.jpg',
        }
        request = self.factory.post(url, data)
        response = add_book_view(request)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)

        # Check if the book is created
        self.assertTrue(Book.objects.filter(title='Test Title').exists())

        # Check if the success message is shown
        messages = list(get_messages(request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Book added successfully.')

    def test_add_book_view_get(self):
        url = reverse('book_routes:add_book_view')
        request = self.factory.get(url)
        response = add_book_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_books.html')
