"""This code defines a custom user manager UserManager by extending the built-in BaseUserManager class in Django. It has two methods - create_user and create_superuser."""
from django.contrib.auth.base_user import BaseUserManager

"""create_user method creates a new user instance with the given email and password, and saves it in the database. It also normalizes the email address and sets the password using the set_password method provided by Django."""
class UserManager(BaseUserManager):
    use_in_migrations =True
    """create_user method creates a new user instance with the given email and password, and saves it in the database. It also normalizes the email address and sets the password using the set_password method provided by Django."""

    def  create_user(self,email,password=None,**kwargs):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user= self.model(email= email, **kwargs)
        user.set_password(password)
        user.save(using=self.db)
        return user
    """create_superuser method calls create_user method and sets the user's is_staff, is_superuser, and is_active fields to True by default. If is_staff is not set to True, it raises a ValueError."""

    def create_superuser(self,email,password,**kwargs):
        kwargs.setdefault('is_staff',True)
        kwargs.setdefault('is_superuser',True)
        kwargs.setdefault('is_active',True)

        if  kwargs.get('is_staff') is not True:
            raise ValueError('Super User must have is_staff true')

        return self.create_user(email,password,**kwargs)
