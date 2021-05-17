from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# 2. agar isgroup true hai to yhaan click hokar sare message aayenge foreign key se

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to="userprofile/", max_length=200, default='userprofile/avatar.png')


class GroupChat(models.Model):
    users = models.ManyToManyField(
        User)
    image = models.ImageField(upload_to="userprofile/",
                              default='userprofile/gp.png')
    name = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=200, default='')


# 1. sabse pehle ye open hoga query curr_user ke self.request.user se hogi,
# DONE
class UserAllChats(models.Model):
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listuser1", blank=True, null=True)
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listuser2", blank=True, null=True)


# 3. agar isgroup false hai to yhaan click hokar sare message aayenge foreign key se user1 ar user2 ke


class PrivateChatMessage(models.Model):
    messageUsername = models.IntegerField()
    message = models.TextField()
    isfile = models.BooleanField(default=False)
    file = models.FileField(upload_to="userprofile/", blank=True, null=True)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user1")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user2")
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)


# 2. agar isgroup true hai to yhaan click hokar sare message aayenge group foreign key se

class GroupChatMessage(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender", blank=True, null=True)
    message = models.TextField()
    isfile = models.BooleanField(default=False)
    file = models.FileField(upload_to="userprofile/", blank=True, null=True)
    group = models.ForeignKey(GroupChat, related_name="groupkey",
                              on_delete=models.CASCADE, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)
