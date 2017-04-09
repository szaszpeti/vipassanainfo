from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.conf import settings
from django.utils import timezone

from  markdown_deux import markdown
from django.utils.safestring import mark_safe

from django.utils.text import slugify

# Create your models here.
class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username






#Post.object.all() (also manager)
#Post.object.create(user=user, title="")etc
# to override them:we this we override Post.objects.all()
#Post.object.all() = super(PostManager, self).all()   at the end YOU HAVE TO LINK IT TO THE MODEL
class PostManager(models.Manager):


    # def all(self, *args, **kwargs):    CHANGE also to ACTIVE in post_list!!!Post.
    def active(self, *args, **kwargs):
        #super(PostManager...is the original call)
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())




def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    #from PostManager
    objects = PostManager()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={'slug': self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

# CONVERT CONTETN TO MARKDOW!!!(HAVE TO INSTALL MARKDOWN-DEUX
    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)


class Document(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:read", kwargs={'slug': self.slug})

    class Meta:
        ordering = ["timestamp", "-updated"]

# CONVERT CONTETN TO MARKDOW!!!(HAVE TO INSTALL MARKDOWN-DEUX
    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)








def create_slug(instance, new_slug=None):
    #slugify the title
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    #check the slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)



#befor saved will go truth this and update our slug

pre_save.connect(pre_save_post_receiver, sender=Post)


def create_document_slug(instance, new_slug=None):
    #slugify the title
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    #check the slug
    qs = Document.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_document_slug(instance, new_slug=new_slug)
    return slug


def pre_save_document_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_document_slug(instance)

pre_save.connect(pre_save_document_receiver, sender=Document)

