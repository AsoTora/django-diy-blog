from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from blog.models import BlogAuthor


# this will basically create a BlogAuthor on creating user

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        BlogAuthor.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.blogauthor.save()
