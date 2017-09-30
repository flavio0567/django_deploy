from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import bcrypt
import re
# Create your models here.


passwd_regex = re.compile(r'^[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z0-9_]+( [a-zA-Z0-9_]+)*$')


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # name and username validation
        if len(postData['name']) < 3: # or
            errors["name"] = "Please enter a valid name - at least 3 characters."
        if not name_regex.match(postData['name']):
            errors["name"] = "Name must contain at least characters."
        if len(postData['username']) < 3: # or not name_regex.match(postData['username']):
            errors["username"] = "Please enter a valid username - at least 3 characters."
        # username validation
        valid_username = User.objects.filter(username = postData['username'])
        if len(valid_username):
            errors["username"] = "There is already an account created with this username. Please either login in using this username, or create an account with a different one."
        # password validation
        if len(postData['passwd1']) < 8:
            errors["password"] = "Please enter a valid name - at least 3 characters."
        if not passwd_regex.match(postData['passwd1']):
            errors["password"] = "Password must contain at least characters."
        else:
            if postData['passwd1'] != postData['passwd2']:
                errors["password"] = "Password did not match. Please try again."
        # return error messages
        return errors


    def login_validator(self, postData):
        context = {'errors' : {}, 'user_name': {}, 'user_id': {}}
        errors = {}
        # validate username
        if postData['username']  == "":
            errors["username"] = "Please enter a valid username"
        if len(postData['username'])  < 3:
            errors["username"] = "Please enter a valid username"
        # validate password
        if postData['passwd']  == "":
            errors["password"] = "Please enter a valid password"
        if len(postData['passwd'])  < 8:
            errors["password"] = "Invalid password, please try again"
            context['errors'] = errors
            return context
        else:
            # user validation
            try:
                user = User.objects.get(username = postData['username'])
            except:
                errors["username"] = "Username not registered, try again."
                context['errors'] = errors
                return context
            if not bcrypt.checkpw(postData['passwd'].encode(), user.password.encode()):
                errors["username"] = "Authentication failed, try again."
                context['errors'] = errors
                return context
            else:
                context['user_name'] = User.objects.get(username = postData['username']).name
                context['user_id'] = User.objects.get(username = postData['username']).id
        # return error messages
        return context


class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        # destination validation
        if postData['destination'] == "":
            errors["destination"] = "Please enter a valid destination - not a empty field"
        # description validation
        if postData['description'] == "":
            errors["description"] = "Please enter a valid description - not a empty field"
        # travel date from validation
        timestamp = datetime.now().strftime("%Y-%m-%d")
        if postData['date_from'] < timestamp:
            errors["date_from"] = "Travel Date should be future-dated. Please try again."
        # travel date to  validation
        if postData['date_to'] < postData['date_from']:
            errors["date_to"] = "Travel 'Date To' should not be before the 'Travel Date From'."
        # return error messages
        return errors


class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return "id: {} name: {} username: {}".format(
            self.id,
            self.name,
            self.username)


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_dt_from = models.DateTimeField()
    travel_dt_to = models.DateTimeField()
    users = models.ManyToManyField(User, related_name = 'joins')
    created_by = models.ForeignKey(User, related_name = 'user')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
    def __str__(self):
        return "{} {} {} {} {}".format(
            self.destination,
            self.description,
            self.travel_dt_from,
            self.travel_dt_to,
            self.created_by)
