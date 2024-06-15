from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid

class User(AbstractUser):
    ROLES = [
        ("Pemerintah", "Pemerintah"),
        ("Petani", "Petani"),
        ("Admin", "Admin")
    ]
    DAERAH = [
        ("Jawa Barat", "Jawa Barat"),
        ("Jawa Tengah", "Jawa Tengah"),
        ("Jawa Timur", "Jawa Timur"),
        ("Jakarta", "Jakarta"),
        ("Banten", "Banten"),
        ("Yogyakarta", "Yogyakarta")
    ]
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=255, blank=False, unique=True)
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255, blank=False, unique=True)
    password = models.CharField(max_length=255, blank=False)
    role = models.CharField(max_length=255, choices=ROLES, default="Petani")
    daerah = models.CharField(max_length=255, choices=DAERAH, blank=False)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set', 
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Changed related_name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

class Pemerintah(models.Model):
    pemerintah_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pemerintah_user')

class Petani(models.Model):
    petani_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='petani_user')

class Admin(models.Model):
    admin_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_user')
