from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .compat import AUTH_USER_MODEL
from .settings import stored_messages_settings


@python_2_unicode_compatible
class Message(models.Model):
    """
    This model represents a message on the database. Fields are the same as in
    `contrib.messages`
    """
    message = models.TextField()
    level = models.IntegerField()
    tags = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    tagged_object = GenericForeignKey('content_type', 'object_id')
    related_history = models.CommaSeparatedIntegerField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['date']


@python_2_unicode_compatible
class MessageArchive(models.Model):
    """
    This model holds all the messages users received. Corresponding
    database table will grow indefinitely depending on messages traffic.
    """
    user = models.ForeignKey(AUTH_USER_MODEL)
    message = models.ForeignKey(Message)

    def __str__(self):
        return "[%s] %s" % (self.user, self.message)


@python_2_unicode_compatible
class Inbox(models.Model):
    """
    Inbox messages are stored in this model until users read them. Once read,
    inbox messages are deleted. Inbox messages have an expire time, after
    that they could be removed by a proper django command. We do not expect
    database table corresponding to this model to grow much.
    """
    user = models.ForeignKey(AUTH_USER_MODEL)
    message = models.ForeignKey(Message)

    class Meta:
        verbose_name_plural = _('inboxes')

    def expired(self):
        expiration_date = self.message.date + timezone.timedelta(
            days=stored_messages_settings.INBOX_EXPIRE_DAYS)
        return expiration_date <= timezone.now()
    expired.boolean = True  # show a nifty icon in the admin

    def __str__(self):
        return "[%s] %s" % (self.user, self.message)
