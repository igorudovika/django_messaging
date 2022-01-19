import json

from django.contrib.auth.models import User
from django.test import TestCase, Client

from messages_application.models import Messages


class ViewsTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.client = Client()
        self.client.login(username='testuser', password='12345')
        Messages.objects.create(title='Hello message', body='hello recipient', recipient_id=user.id, sender_id=user.id)

    def test_main_page_without_auth(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')

    def test_main_page_with_auth(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_404_page(self):
        response = self.client.get("/some/")
        self.assertEqual(response.status_code, 404)

    def test_api_get_inbox(self):
        response = self.client.get("/api/inbox/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Hello message')

    def test_api_post_inbox(self):
        response = self.client.post("/api/inbox/")
        self.assertEqual(response.status_code, 405)

    def test_api_get_inbox_id(self):
        response = self.client.get("/api/inbox/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Hello message')

    def test_api_post_inbox_id(self):
        response = self.client.post("/api/inbox/1/")
        self.assertEqual(response.status_code, 405)

    def test_api_put_inbox_id(self):
        response = self.client.put("/api/inbox/1/", data=json.dumps({'id': 1,
                                                                     'title': 'first message',
                                                                     'body': 'Hello my frend',
                                                                     'sender': 1,
                                                                     'recipient': 1}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Messages.objects.all().count(), 1)
        self.assertEqual(Messages.objects.first().title, 'first message')
        self.assertEqual(Messages.objects.first().body, 'Hello my frend')

    def test_api_delete_inbox(self):
        response = self.client.delete("/api/inbox/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Messages.objects.all().count(), 0)

    def test_api_get_sent(self):
        response = self.client.get("/api/sent/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Hello message')

    def test_api_get_sent_id(self):
        response = self.client.get("/api/sent/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Hello message')

    def test_api_post_sent(self):
        response = self.client.post("/api/sent/",
                                    data=json.dumps({'title': 'One more hello message', 'body': 'hello recipient',
                                                     'recipient': 1,
                                                     'user': '{id: 1}'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Messages.objects.all().count(), 2)
        self.assertEqual(Messages.objects.last().title, 'One more hello message')

    def test_api_post_sent_id(self):
        response = self.client.post("/api/sent/1/")
        self.assertEqual(response.status_code, 405)

    def test_api_put_sent_id(self):
        response = self.client.put("/api/sent/1/", data=json.dumps({'id': 1,
                                                                    'title': 'first message',
                                                                    'body': 'Hello my frend',
                                                                    'sender': 1,
                                                                    'recipient': 1}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Messages.objects.all().count(), 1)
        self.assertEqual(Messages.objects.first().title, 'first message')
        self.assertEqual(Messages.objects.first().body, 'Hello my frend')

    def test_api_delete_sent(self):
        response = self.client.delete("/api/sent/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Messages.objects.all().count(), 0)

    def test_api_get_users(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser')

    def test_api_post_users(self):
        response = self.client.post("/api/users/")
        self.assertEqual(response.status_code, 405)
