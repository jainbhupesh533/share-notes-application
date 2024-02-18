import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom User Manager class for the User Model
    """

    def create_user(self, **kwargs):
        user = self.model(
            full_name=kwargs.get('full_name'),
            user_name=kwargs.get('user_name'),
            is_active=True
        )

        user.set_password(kwargs.get('password'))
        user.save()
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user

    def create_admin_user(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_admin = True
        user.save()
        return user

    def create_staff_user(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_staff = True
        user.save()
        self.assign_user_to_group(user)
        return user


class User(AbstractBaseUser):
    """
    User model to define every user of Enguru

    Every Actor is has a user model with which their User Profile is linked
    is_admin: Identifies if the user is an admin user
    is_staff: Identifies if the user is a staff user
    created_at: The date on which the account was created
    updated_at: The date on which the account was updated
    """
    full_name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)
    user_name = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    class Meta:
        db_table = 'user'

    USERNAME_FIELD = 'id'

    def __unicode__(self):
        return self.id

    def __str__(self):
        return f'{self.id} - {str(self.full_name)}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_superuser(self):
        if self.is_admin and self.is_staff:
            return True
        return False