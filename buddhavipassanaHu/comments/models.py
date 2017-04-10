from django.db import models
from django.conf import settings


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        # this will be like this Document.objects.get(id=instance.id)
        obj_id = instance.id
        # super(CommentManager, self) ==== Comments.object.
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        # comments = Comments.objects.filter
        return qs


# after this hva to add objects = CommentManager() in the class below


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    #document = models.ForeignKey(Document)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    def __str__(self):
        return str(self.user.username)
