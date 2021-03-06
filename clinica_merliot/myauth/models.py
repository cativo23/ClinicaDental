from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(username=username,
                          email=self.normalize_email(email), )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(username, email, password=password,)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    MALE= 'M'
    FEMALE = "F"
    NO = "N"
    SEX_CHOICES = (
        (MALE, 'Masculino'),
        (FEMALE, 'Femenino'),
        (NO, "No decir"),
    )
    username = models.CharField('Nombre de usuario', max_length=25, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=100,
        unique=True,
    )
    sex = models.CharField(max_length=2, choices=SEX_CHOICES, blank=False, null=False, default="N")
    avatar = models.ImageField(blank=True, null=True, upload_to='profiles/')
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['username']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    #def avatar(self):
    #    return '<a href="{0}{1}"><img src="{0}{1}" style="height:100px;width:100px;"  ></a>'.format(settings.MEDIA_URL, self.avatar.url)

#    //avatar.short_description = 'Image'
#    avatar.allow_tags = True
