"""Manager class"""

from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    """
    Handles Ticketing users creation.
    """
    use_in_migrations =True


    def  create_user(self,email,password=None,**kwargs):
        """
        Creates an Eventgoer user account
        :param email: email to create the user with
        :param password: password to create the new user with
        :param kwargs: (Passed to the model)
        :return:
        """
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user= self.model(email= email, **kwargs)
        user.set_password(password)
        user.save(using=self.db)
        return user


    def create_superuser(self,email,password,**kwargs):
        """
        (DO NOT USE! UNSECURE!) Creates a superuser Eventgoer account
        :param email: email to create the user with
        :param password: password to create the new user with
        :param kwargs: is_staff, is_superuser, is_active
        :return: the newly created user
        """
        kwargs.setdefault('is_staff',True)
        kwargs.setdefault('is_superuser',True)
        kwargs.setdefault('is_active',True)

        if  kwargs.get('is_staff') is not True:
            raise ValueError('Super User must have is_staff true')

        return self.create_user(email,password,**kwargs)
