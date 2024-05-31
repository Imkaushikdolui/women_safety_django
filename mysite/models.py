from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

class MyAccountManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, name, email, username, password=None, **extra_fields):
        if not name:
            raise ValueError("User must have a name")
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")

        email = self.normalize_email(email)
        user = self.model(
            name=name,
            email=email,
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, username, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(name, email, username, password, **extra_fields)

class Account(AbstractBaseUser):
    name = models.CharField(verbose_name="name", max_length=30, null=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Contact(models.Model):
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="contacts", null=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=15)
    
    # Relation choices
    FATHER = "Father"
    MOTHER = "Mother"
    BROTHER = "Brother"
    SISTER = "Sister"
    HUSBAND = "Husband"
    FRIEND = "Friend"
    RELATIVE = "Relative"
    OTHER = "Other"
    
    RELATION_CHOICES = (
        (FATHER, "Father"),
        (MOTHER, "Mother"),
        (BROTHER, "Brother"),
        (SISTER, "Sister"),
        (HUSBAND, "Husband"),
        (FRIEND, "Friend"),
        (RELATIVE, "Relative"),
        (OTHER, "Other"),
    )
    
    relation = models.CharField(max_length=10, choices=RELATION_CHOICES, default=OTHER)

    def __str__(self):
        return self.name  # This is correct for a SOS application to display contact names.
