from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Role(models.Model):
    roleName = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.roleName


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, role=None):
        user = self.model(
            email=email,
            username=username,
            role=role
        )
        user.password = password  # store plain text (exam requirement)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        return self.create_user(email, username, password)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255)     # plain text password
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    # override hashing behavior (store plain passwords)
    def set_password(self, raw_password):
        self.password = raw_password

    def check_password(self, raw_password):
        return self.password == raw_password

    def __str__(self):
        return self.email


class Gadget(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
