from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class ResidentManager(BaseUserManager):
    def create_user(self, room_number, first_name, last_name, password=None):
        if not room_number:
            raise ValueError('Residents must have a room number')
        if not first_name:
            raise ValueError('Residents must have a first name')
        if not last_name:
            raise ValueError('Residents must have a last name')

        user = self.model(
                room_number = room_number,
                first_name = first_name,
                last_name = last_name,
                )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, room_number, first_name, last_name, password=None):
        user = self.create_user(
                room_number = room_number,
                first_name = first_name,
                last_name = last_name,
                password=password,
                )

        user.is_admin       = True
        user.is_staff       = True
        user.is_superuser   = True

        user.save(using=self._db)
        return user


class Resident(AbstractBaseUser):
    room_number     = models.CharField(max_length=3, primary_key=True, unique=True)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)

    username        = None
    email           = None
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)

    is_active       = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)

    USERNAME_FIELD  = 'room_number'
    REQUIRED_FIELDS = [
            'first_name',
            'last_name',
            ]

    objects = ResidentManager()

    def __str__(self):
        return self.room_number

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class WashTime(models.Model):
    start_time  = models.DateTimeField()
    end_time    = models.DateTimeField()
    resident    = models.ForeignKey(Resident, on_delete=models.CASCADE)


