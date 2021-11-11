from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from django.db import models
from channels.layers import get_channel_layer


class Messages(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='recipient', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    body = models.TextField()

    def save(self, *args, **kwargs):
        """
        Calls super one plus sends message into websocket that model was changed, so UI refresh is needed
        """
        super(Messages, self).save(*args, **kwargs)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'render_updates_group',
            {'type': 'send_message_to_frontend',
             'message': 'Message was updated'})

    def delete(self, *args, **kwargs):
        """
        Calls super one plus sends message into websocket that model was changed, so UI refresh is needed
        """
        super(Messages, self).delete(*args, **kwargs)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'render_updates_group',
            {'type': 'send_message_to_frontend',
             'message': 'Message was deleted'})
