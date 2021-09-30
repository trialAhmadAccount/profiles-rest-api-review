from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager 


class UserProfileManager(BaseUserManager):
    """""Manager to manipulate the User that is made for"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email: 
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)  

        user.set_password(password)    
        user.save(using=self._db)  #saving Django objects to db
        #This line means you can support multiple dbs   
        return user 

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)  

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)  

        return user             
        

class UserProfile(AbstractBaseUser, PermissionsMixin): #Base class and mixin can be used inside the class to customize it 
    """"Database model for users in the system"""

    email = models.EmailField(max_length=255, unique=True) #Each user has unique email
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff =  models.BooleanField(default=False)

    # Custome model mannager to be used for objects
    #Required to know how to create users and control them using cmd of Django

    objects = UserProfileManager()

    #These are needed to work with Django admin and auth system 

    USERNAME_FIELD = 'email' #Replace the username used for auth by default from Django by our email implementation
    REQUIRED_FIELDS = ['name']

    #Required funs used for django to interact with custom model

    def get_full_name(self):
        """"" Retrieve full name of user """
        return self.name

    def get_short_name(self):
        """"" Retrieve short name of user """
        return self.name         


    #Item to return UserProfile object as a String 

    def __str__(self):
        """""Return string representation of our user"""
        return self.email
