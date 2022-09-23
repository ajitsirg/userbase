
# from django.contrib.auth.models import AbstractUser
# from django.db import models

# from .manager import UserManager

# gender_option=   (("male", "Male"),("female", "Female"))

# class User(AbstractUser):
#     username = None
#     name = models.CharField(max_length=255,blank=True,null=True)
#     email = models.EmailField(unique=True)
#     mobile_number=models.IntegerField(max_length=14,unique=True)
#     address = models.CharField(max_length=1000,blank=True,null=True)
#     city = models.CharField(max_length=255,blank=True,null=True)
#     state = models.CharField(max_length=255,blank=True,null=True)
#     pincode = models.IntegerField(max_length=6,blank=True,null=True)
#     gender=models.CharField(max_length=10 ,choices=gender_option,default='male')
#     last_login = models.DateTimeField(blank=True,null=True)
#     last_logout = models.DateTimeField(blank=True,null=True)
#     last_ip = models.GenericIPAddressField(protocol='IPv4', verbose_name="Last Login IP")
    
#     is_verify = models.BooleanField(default=False)
    
#     is_student = models.BooleanField(default=False)
#     is_teacher = models.BooleanField(default=False)
#     is_vendor = models.BooleanField(default=False)
#     is_coustmer = models.BooleanField(default=False)
    
#     USERNAME_FIELD= 'email'
    
#     objects= UserManager
    
#     REQUIRED_FIELDS = ['password']



# class Subject(models.Model):
#     sub1= models.CharField(max_length=10, null=True, blank=True)
#     sub2= models.CharField(max_length=20, null=True, blank=True)




# class Quiz(models.Model):
#     quiz1= models.CharField(max_length=10, null=True, blank=True)
#     quiz2= models.CharField(max_length=20, null=True, blank=True)    
    
    
# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     # quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
#     interests = models.ManyToManyField(Subject, related_name='interested_students')
    
    
    
# class Teacher(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     # quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
#     interests = models.ManyToManyField(Subject, related_name='interested_Teacher')    

    
    
    

import random
import string
import uuid

from django.core.validators import RegexValidator, MinValueValidator

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,  PermissionsMixin)
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,)
from django.utils.crypto import salted_hmac
from . manager import UserManager
# from django.utils.translation import ugettext_lazy as _


gender_option=   (("male", "Male"),("female", "Female"))



class BaseUser(models.Model):
    email = models.EmailField(unique=True, max_length=50)
    password = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True, help_text=(
        'date format: yyyy-mm-dd    ex:2018-11-15'))
    mobile_number = models.CharField(max_length=30)
    alternate_number = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(
        max_length=100, blank=True, null=True, choices=gender_option)
    is_staff = models.BooleanField(default=False, help_text=(
        'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(default=False,
                                    help_text=(
                                        'Designates whether this user should be treated as active. '
                                        'Unselect this instead of deleting accounts.'
                                    ),
                                    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    registered_by = models.EmailField(max_length=255, null=True, blank=True)

    _password = None

    class Meta:
        abstract = True

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        """
        Return False if set_unusable_password() has been called for this user.
        """
        return is_password_usable(self.password)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()


# Custom User with extended group permissions functionality


class User(AbstractBaseUser, PermissionsMixin):

    """
    Email, password, user type, mobile number are required. Other fields are optional.
    """

    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20, )
    middle_name = models.CharField(
        max_length=20, blank=True, null=True, )
    last_name = models.CharField(max_length=20, )
    email = models.EmailField(unique=True, max_length=255)
    mobile_number = models.CharField(
         blank=False, max_length=10, unique=True)
    alternate_number = models.CharField(max_length=30, blank=True, null=True)
    active = models.BooleanField(default=False,
                                 help_text=(
                                     'Designates whether this user should be treated as active. '
                                     'Unselect this instead of deleting accounts.'
                                 ),
                                 )  # can login
    staff = models.BooleanField(default=False, help_text=(
        'Designates whether the user can log into this admin site.'))  # staff user non superuser
    superuser = models.BooleanField(default=False)  # superuser

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    user_type = models.CharField(
        max_length=25, choices=gender_option)

    date_of_birth = models.DateField(blank=True, null=True, help_text=(
        'date format: yyyy-mm-dd    ex:2018-11-15'))

    gender = models.CharField(
        max_length=100, blank=True, null=True, choices=gender_option)

    USERNAME_FIELD = 'email'  # username

    REQUIRED_FIELDS = ['user_type', 'mobile_number']

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.get_short_name

    @property
    def full_name(self):
        "Returns the person's full name."
        if self.middle_name is None and self.last_name is not None:
            return '%s %s' % (self.first_name, self.last_name)
        elif self.middle_name is not None and self.last_name is None:
            return '%s %s' % (self.first_name, self.middle_name)
        elif self.middle_name is not None and self.last_name is not None:
            return '%s %s %s' % (self.first_name, self.middle_name, self.last_name)

        return self.first_name

    @property
    def get_short_name(self):
        "Returns the person's short name to show after welcome on UI."
        if self.full_name:
            return self.full_name
        elif self.first_name:
            return self.first_name
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_superuser(self):
        return self.superuser

    def save(self, *args, **kwargs):
        print("Saving new user for admin panel : " + str(self))
        super(User, self).save(*args, **kwargs)

    