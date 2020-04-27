from django.db import models
import re
import bcrypt
from datetime import datetime, date

# Create your models here.

class UserManager(models.Manager):
    def userValidator(self,postData):
        errors = {}
        if len(postData['name'])<3:
            errors['name'] = "Name of at least 3 characters required!"
        if len(postData['reg_username'])<3:
            errors['reg_username'] = "Username of at least 3 characters required!"
# password Validation
        if postData['reg_pw'] != postData['confirm_pw']:
            errors['reg_pw'] = "Password does not match!"

        elif len(postData['reg_pw'])<8:
            errors['reg_pw'] = "Password needs to be at least 8 characters"
        return errors

    def loginValidator(self, postData):
        errors = {}
        # log In errors
        usernameMatch = User.objects.filter(username = postData['username'])
        
        if len(postData['username'])<1:
            errors['username'] = "Enter your registered Username to Log In"
# username validation on login
        elif len(usernameMatch) == 0:
            errors['Username does not exist'] = "Invalid username, please use another Username or register!"
        # if the username is valid, verify if password match
        else:
            user = usernameMatch[0]
            if not bcrypt.checkpw(postData['login_pw'].encode(), user.password.encode()):
                errors['login_pw'] = "Password does not match"

        return errors

class tripManager(models.Manager):
    def tripValidator(self, postData):
        errors = {}
        if len(postData['destination'])<1:
            errors['destination'] = "Destination is required"
        if len(postData['description'])<1:
            errors['description'] = "Description is required"
        # date validation

        currentDate = date.today()
        start_date = datetime.strptime(postData['travel_from'], "%Y-%m-%d").date()
        end_date = datetime.strptime(postData['travel_to'], "%Y-%m-%d").date()
        print(currentDate)
        print(start_date)
        print(end_date)

        if start_date < currentDate:
            errors['start'] = "Invalid Travel start date. Please provide upcoming travel dates."
        elif end_date < currentDate:
            errors['end'] = "Invalid Travel end date. Please provide upcoming travel dates."
        elif start_date > end_date:
            errors['end'] = "Invalid Travel end date. Start date cannot begin after end date."
        
        print(errors)
        return errors



class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=75)
    confirm_password = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Travelplans(models.Model):
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    uploader = models.ForeignKey(User, related_name = "uploaded_by", on_delete = models.CASCADE)
    favorite = models.ManyToManyField(User, related_name= "favorite")
    travel_start = models.DateField(auto_now_add=False)
    travel_end = models.DateField(auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True, null = True)
    updated_at = models.DateTimeField(auto_now=True, null = True)
    objects = tripManager()
