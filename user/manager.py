
# from django.contrib.auth.base_user import BaseUserManager



# class UserManager(BaseUserManager):
#     use_in_migrations: True
    
    
#     def create_user(self,email,password=None,**extra_fields):
        
#         if not email:
#             raise ValueError('email must not be empty')
        
#         email =self.normalize_email(email)
#         user =self.model(email=email,**extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
    
#     def create_superuser(self,email,password,**extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)
        
        
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError(('Superuser must have staff permission'))
        
#         return self.create_user(email,password,**extra_fields)
            
        
        
        
        
from django.contrib.auth.models import (
    BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, email, mobile_number, user_type, password=None, is_staff=False, is_superuser=False, is_active=False):

        print('creating a non-active, non-superuser and non-staff user')

        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")
        if not user_type:
            raise ValueError("User must have a user type")
        if not mobile_number:
            raise ValueError("User must have a mobile number")
        user_obj = self.model(
            email=self.normalize_email(email)
        )

        user_obj.set_password(password)  # set or change password
        user_obj.staff = is_staff
        user_obj.superuser = is_superuser
        user_obj.active = is_active
        user_obj.mobile_number = mobile_number
        user_obj.user_type = user_type

        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, mobile_number, user_type, password=None):

        print('creating a staff user')

        user = self.create_user(
            email=email,
            password=password,
            mobile_number=mobile_number,
            user_type=user_type,
            is_staff=True,
            is_active=True
        )
        return user

    def create_superuser(self, email, mobile_number, user_type, password=None):

        print('creating a super user')

        user = self.create_user(
            email=email,
            password=password,
            mobile_number=mobile_number,
            user_type=user_type,
            is_staff=True,
            is_active=True,
            is_superuser=True
        )
        return user

    def get_user_by_user_type(self, user_type):
        return self.get_queryset().filter(user_type=user_type)

    def get_user_by_email(self, email):
        return self.get_queryset().filter(email=email)

    def get_group_permissions(self):
        return self._get_queryset_methods(obj=None)
            