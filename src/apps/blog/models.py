from django.db import models
from django.contrib.auth.models import User

from django.utils.text import slugify
from uuid import uuid4
from os import path


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


def post_directory_path(instance, filename):
    user = instance.post.owner
    post = instance.post
    file = str(uuid4())[:8] + path.splitext(filename)[1]
    return f'user-{user.username}/posts/{post.slug}/{file}'


class PostImage(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    data = models.ImageField(upload_to=post_directory_path)

    class Meta:
        verbose_name = 'Post Image'
        verbose_name_plural = 'Posts Images'
