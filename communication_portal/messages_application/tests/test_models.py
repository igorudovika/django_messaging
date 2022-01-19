from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth.models import User

from messages_application.models import Messages


class ModelsTestCase(TestCase):
    def setUp(self):
        self.recipient = User.objects.create(username='recipient')
        self.recipient.save()
        self.sender = User.objects.create(username='sender')
        self.sender.save()

    def create_simple_talk(self):
        message = Messages.objects.create(title='Hello message', body='hello recipient', recipient_id=self.recipient.id,
                                          sender_id=self.sender.id)
        message.save()
        self.assertEqual(Messages.objects.all().count(), 1)
        message = Messages.objects.create(title='Hello reply', body='hello sender', recipient_id=self.sender.id,
                                          sender_id=self.recipient.id)
        message.save()
        self.assertEqual(Messages.objects.all().count(), 2)

    def test_main_flow(self):
        self.create_simple_talk()

    def test_delete_message(self):
        self.create_simple_talk()
        message = Messages.objects.first()
        message.delete()
        self.assertEqual(Messages.objects.all().count(), 1)

    def test_missed_title(self):
        message = Messages.objects.create(body='hello one more time', recipient_id=self.recipient.id,
                                          sender_id=self.sender.id)
        message.save()
        self.assertEqual(Messages.objects.all().count(), 1)

    def test_missed_body(self):
        message = Messages.objects.create(title='Hello message', recipient_id=self.recipient.id,
                                          sender_id=self.sender.id)
        message.save()
        self.assertEqual(Messages.objects.all().count(), 1)

    def test_missed_recipient(self):
        with self.assertRaises(IntegrityError):
            message = Messages.objects.create(title='Hello message', body='hello recipient', sender_id=self.sender.id)
            message.save()

    def test_missed_sender(self):
        with self.assertRaises(IntegrityError):
            message = Messages.objects.create(title='Hello message', body='hello recipient',
                                              recipient_id=self.recipient.id)
            message.save()
