from ..base import StoredMessagesBackend
from ..exceptions import MessageTypeNotSupported, MessageDoesNotExist
from ...models import Inbox, Message, MessageArchive
from django.db import models
from django.contrib.contenttypes.models import ContentType

class DefaultBackend(StoredMessagesBackend):
    """

    """
    def inbox_list(self, user):
        if user.is_anonymous():
            return []
        inbox = Inbox.objects.filter(user=user).select_related("message")
        return [m.message for m in inbox]

    def inbox_purge(self, user):
        if user.is_authenticated():
            Inbox.objects.filter(user=user).delete()

    def inbox_store(self, users, msg_instance):
        if not self.can_handle(msg_instance):
            raise MessageTypeNotSupported()

        for user in users:
            Inbox.objects.get_or_create(user=user, message=msg_instance)

    def inbox_delete(self, user, msg_id):
        try:
            inbox_m = Inbox.objects.filter(user=user, message=msg_id).get()
            inbox_m.delete()
        except Inbox.DoesNotExist:
            raise MessageDoesNotExist("Message with id %s does not exist" % msg_id)

    def inbox_get(self, user, msg_id):
        try:
            return Inbox.objects.get(pk=msg_id).message
        except Inbox.DoesNotExist:
            raise MessageDoesNotExist("Message with id %s does not exist" % msg_id)

    def create_message(self, level, msg_text, extra_tags='', **kwargs):
        m_instance = Message.objects.create(message=msg_text, level=level, tags=extra_tags, **kwargs)
        return m_instance

    def archive_store(self, users, msg_instance):
        if not self.can_handle(msg_instance):
            raise MessageTypeNotSupported()

        for user in users:
            MessageArchive.objects.create(user=user, message=msg_instance)

    def archive_list(self, user):
        if user.is_anonymous():
            return []
        archive = MessageArchive.objects.filter(user=user).select_related("message")
        return [m.message for m in archive]

    def archive_get(self, user, msg_id):
        try:
            return MessageArchive.objects.get(pk=msg_id).message
        except MessageArchive.DoesNotExist:
            raise MessageDoesNotExist("Message with id %s does not exist" % msg_id)

    def can_handle(self, message):
        return isinstance(message, Message)

    def _flush(self):
        Inbox.objects.all().delete()
        MessageArchive.objects.all().delete()
        Message.objects.all().delete()
