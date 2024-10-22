from django.core.management.base import BaseCommand
from account.models import User  # Adjust to your app name
from django.utils import timezone
import random
import string

class Command(BaseCommand):
    help = 'Create bulk random users and trigger signals'

    def add_arguments(self, parser):
        parser.add_argument('num_users', type=int, help='Number of users to create')

    def handle(self, *args, **kwargs):
        num_users = kwargs['num_users']

        for i in range(num_users):
            first_name = "sourabh"
            last_name = "das"
            email = f'{first_name}.{last_name}{self.random_string(7)}@example.com'.lower()
            password = 'password123'  # A default password

            # Create the user object without saving yet
            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            # Set the password and username
            user.set_password(password)
            user.username = user.generate_unique_username()

            # Save the user (this will trigger signals and any logic in the save() method)
            user.save()

            # If you want to log in the user programmatically, you could add login logic here
            # For example: login(request, user)

            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {email}'))

        self.stdout.write(self.style.SUCCESS(f'{num_users} users created successfully.'))

    def random_string(self, length):
        # Generate a random string of letters
        return ''.join(random.choices(string.ascii_lowercase, k=length))
