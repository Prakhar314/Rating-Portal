from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    bannedTill = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True,null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomUserModel.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.customusermodel.save()
