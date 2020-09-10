from django.db import models
from django.contrib.auth.models import (
                                        AbstractBaseUser,
                                        BaseUserManager
                                        )


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None ,password=None, is_active=True):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")
        # if not full_name:
        #     raise ValueError("User must have a fullname")
        user = self.model(email = self.normalize_email(email),
                          full_name = full_name
        )

        user.set_password(password) #change user password

        user.save(using = self._db)
        return user

    def create_staffuser(self, email, full_name=None, password=None):
        user = self.create_user(email,full_name=full_name, password=password)
        user.is_staff= True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name=None, password= None):
        user = self.create_user(email,full_name=full_name, password=password)
        user.is_staff = True
        user.admin = True
        user.save(using = self._db)
        return user


class User(AbstractBaseUser):
    """creating custom user model with an email field"""
    email           = models.EmailField(max_length=255, unique=True)
    full_name       = models.CharField(max_length=255, blank=True,null=True)
    is_active       = models.BooleanField(default=True) #can login
    is_staff        = models.BooleanField(default=False) #staffuser not super user
    admin           = models.BooleanField(default=False)
    timestamp       = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'    #username

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # @property
    # def is_staff(self):
    #     return self.staff
    #
    # @property
    # def is_active(self):
    #     return self.active
    #
    @property
    def is_admin(self):
        return self.admin


class GuestModel(models.Model):
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
