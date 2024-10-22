from django.core.management.base import BaseCommand
from account.models import User  # Import your User model

class Command(BaseCommand):
    help = 'Assign usernames to users who do not have one.'

    def handle(self, *args, **kwargs):
        users_without_username = User.objects.filter(username__isnull=True)

        for user in users_without_username:
            user.username = user.generate_unique_username()  # Use the method you defined
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Assigned username "{user.username}" to user {user.email}'))

        if not users_without_username.exists():
            self.stdout.write(self.style.SUCCESS('All users already have a username.'))




# python manage.py assign_usernames
