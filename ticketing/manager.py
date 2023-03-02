"""Manager class"""

from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations =True


    def  create_user(self,email,password=None,**kwargs):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user= self.model(email= email, **kwargs)
        user.set_password(password)
        user.save(using=self.db)
        return user


    def create_superuser(self,email,password,**kwargs):
        kwargs.setdefault('is_staff',True)
        kwargs.setdefault('is_superuser',True)
        kwargs.setdefault('is_active',True)

        if  kwargs.get('is_staff') is not True:
            raise ValueError('Super User must have is_staff true')

        return self.create_user(email,password,**kwargs)
