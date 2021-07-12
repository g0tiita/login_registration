from django.db import models
import re

# Manejador del usuario
class UserManager(models.Manager):
    def basic_validator(self, postData):
        EMAIL_REGEX = re.compile(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+')
        ONLYLETTERS_REGEX = re.compile(r'^[A-Z][a-z]+$')

        errors = {}
        # agregue claves y valores al diccionario de errores para cada campo no válido
        if len(postData['firstname']) < 2:
            errors['firstname'] = "Firstname should be at least 2 characters"
        
        if len(postData['lastname']) < 2:
            errors['lastname'] = "Last description should be at least 2 characters"
        
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        
        if not ONLYLETTERS_REGEX.match(postData['firstname']) or not ONLYLETTERS_REGEX.match(postData['lastname']):
            errors['email'] = "Only letters in firstname and lastname"    
        
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 chatacteres"

        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Password and password confirm not match"
        
        return errors

# Modelo de Usuario
class User(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=70)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    
    def __repr__(self):
        return f"{self.firstName} {self.lastName}"

    