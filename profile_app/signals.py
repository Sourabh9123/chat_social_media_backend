from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import User
from profile_app.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile whenever a new User is created."""
    print("""Create a Profile whenever a new User is created.""")
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the Profile whenever the User is saved."""
    print( """Save the Profile whenever the User is saved.""")
    instance.profile.save()