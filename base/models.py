from django.db import models
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Base(models.Model):
    class Meta:
        ordering = ["-pk"]
        verbose_name_plural = "Basics"

    created_time = models.DateTimeField(db_index=True, default=now, editable=False, blank=True)
    updated_time = models.DateTimeField(db_index=True, default=now, blank=True)


class HashtagParent(Base):
    title = models.CharField(db_index=True, max_length=50, help_text='String(50)')


class Hashtag(Base):
    title = models.CharField(db_index=True, max_length=50, help_text='String(50)')
    related_parent = models.ForeignKey(HashtagParent, related_name='nested_mentions', blank=True, null=True, db_index=True, on_delete=models.CASCADE, help_text='String(50)')
    hashtag_base = models.ForeignKey(Base, related_name='base_hashtags', on_delete=models.CASCADE, blank=True, null=True, db_index=True, help_text='Integer')


class BaseComment(Base):
    comment_parent = models.ForeignKey(Base, related_name='base_comments', db_index=True, on_delete=models.CASCADE, help_text='Integer')
    comment_sender = models.ForeignKey('users.Identity', related_name='base_comment_senders', db_index=True, on_delete=models.CASCADE, help_text='Integer')
    comment_picture = models.ForeignKey('media.Media', on_delete=models.CASCADE, related_name="base_comment_picture", help_text='Integer')
    text = models.TextField(help_text='Text')