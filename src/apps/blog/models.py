from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible

from django.utils.text import slugify
from uuid import uuid4
from os import path

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageFilter
from io import BytesIO
import sys


class Category(models.Model):

    name = models.CharField(max_length=128)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Post(models.Model):

    STATUS_CHOICES = [
        ('D', 'draft'),
        ('P', 'published')
    ]

    DEFAULT_USER_PK = 1

    title = models.CharField(max_length=128)
    slug = models.SlugField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    content = models.TextField()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        default=DEFAULT_USER_PK
    )

    categories = models.ManyToManyField(
        Category,
        related_name='posts',
        blank=True
    )

    def save(self, *args, **kwargs):
        self.slug = self.slug if self.slug else slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


@deconstructible
class UploadPostImagesPath:

    def __init__(self, postfix):
        self.postfix = postfix

    def __call__(self, instance, filename):
        user = instance.post.owner
        post = instance.post
        file = f'{str(uuid4())[:8]}-{self.postfix}{path.splitext(filename)[1]}'
        return f'user-{user.username}/posts/{post.slug}/{file}'


class PostImage(models.Model):

    SM_PATH = UploadPostImagesPath('sm')
    LG_PATH = UploadPostImagesPath('lg')
    SM_IMG_SIZE = (400, 400)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    small = models.ImageField(upload_to=SM_PATH, blank=True, null=True)
    large = models.ImageField(upload_to=LG_PATH, blank=True, null=True)

    def save(self, *args, **kwargs):

        im = Image.open(self.large)
        output = BytesIO()

        im.thumbnail(self.SM_IMG_SIZE)
        im.save(output, format='JPEG')
        output.seek(0)

        self.small = InMemoryUploadedFile(
            output,
            'ImageField',
            'tmp.jpg',
            'image/jpeg',
            sys.getsizeof(output),
            None
        )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Post Image'
        verbose_name_plural = 'Posts Images'
