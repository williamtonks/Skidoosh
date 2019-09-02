import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey, TreeOneToOneField
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    registration_date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='images/profile_pictures/', default='/static/images/profile_pictures/default_profile_picture.png')
    year_choices = [('1st Year', '1st Year'), ('2nd Year', '2nd Year'), ('3rd Year', '3rd Year'),
                    ('4th Year', '4th Year'), ('Grad', 'Graduate Student'), ('Alumni', 'Alumni')]
    year = models.CharField(max_length=50, choices=year_choices)
    bio = models.TextField(max_length=500)
    phonenumber = models.CharField('Phone Number', max_length=20, default=0)
    groups = models.ManyToManyField('InterestGroup')
    posts = models.ManyToManyField('GroupPost')

    class Meta:
        ordering = ['name', 'registration_date']

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class InterestGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='images/groups/thumbnails', default='images/groups/thumbnails/default_thumbnail.jpg')

    class Meta:
        ordering = ['name', 'description']

    def __str__(self):
        return self.name


class GroupPost(MPTTModel):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, )
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=500)
    interest_group = models.ForeignKey('InterestGroup', on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    likes = models.ManyToManyField('Profile', related_name='liked_posts')

    class MPTTMeta:
        order_insertion_by = ['-creation_date']


class DiscussionPost(GroupPost):
    title = models.CharField(max_length=100)


class EventPost(GroupPost):
    title = models.CharField(max_length=100)
    event_date = models.DateField()
    attending = models.ManyToManyField('Profile')


class Comment(GroupPost):
    pass;

