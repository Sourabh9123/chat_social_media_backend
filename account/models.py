from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid
import random
import string



class UserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            first_name = first_name,
            last_name = last_name,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name,**extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name,**extra_fields):
        user = self._create_user(email, password,first_name, last_name, True, True, **extra_fields)
        return user
    

    


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # username = models.CharField(max_length=254, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)  
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    email_verified =models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', "last_name"]

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    
    def save(self, *args, **kwargs):
        if not self.username:  # Check if username is not set
            self.username = self.generate_unique_username()
        super().save(*args, **kwargs)


    def generate_unique_username(self):
        # Generate a unique username based on first and last name or random string
        base_username = f"{self.first_name.lower()}_{self.last_name.lower()}"
        unique_username = base_username

        # Check if username exists, and if it does, append a random number
        while User.objects.filter(username=unique_username).exists():
            unique_username = f"{base_username}{''.join(random.choices(string.ascii_lowercase + string.digits, k=4))}"

        return unique_username
    
