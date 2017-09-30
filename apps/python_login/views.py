from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import User
from .models import Trip
import bcrypt

# Create your views here.
def home(request):
    return render(request, 'python_login/login.html')


def check_login(request):
    # login credentials validation
    context = User.objects.login_validator(request.POST)
    errors = context['errors']
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return render(request, 'python_login/login.html')
    request.session['user_id'] = context['user_id']
    return redirect("/travels")


def travels(request):
    # getting travels related to user
    user = User.objects.get(id=request.session['user_id'])
    context = {
            "user": user,
            "travels_user": Trip.objects.filter(created_by=user),
            "travels_join": Trip.objects.filter(users=user),
            "travels_others": Trip.objects.exclude(created_by=user).exclude(users=user)
        }
    return render(request, 'python_login/travel.html', context)


def check_register(request):
    # validation & creation of a new user
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return render(request, 'python_login/login.html')
    else:
        hashed = bcrypt.hashpw((request.POST['passwd1'].encode()), bcrypt.gensalt(5))
        User.objects.create(
            name=request.POST['name'],
            username=request.POST['username'],
            password=hashed
        )
        request.session['user_id'] = User.objects.last().id
    return redirect('/travels')


def travels_add(request):
    # add a new travel
    return render(request, 'python_login/travel_add.html')


def check_travel(request):
    # validation & creation of a new travels
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return render(request, 'python_login/travel_add.html')
    else:
        user=request.session['user_id']
        user_trip=User.objects.get(id=user)
        # create a new travel
        Trip.objects.create(
            destination=request.POST['destination'],
            description=request.POST['description'],
            travel_dt_from=request.POST['date_from'],
            travel_dt_to=request.POST['date_to'],
            created_by=user_trip
        )
    return redirect("/travels")


def show(request, id):
    # show travels
    trip = Trip.objects.get(id=id)
    context = {
        "user" : trip.created_by,
        "travel" : Trip.objects.get(id=id),
        "users" : User.objects.filter(joins=trip)
    }
    return render(request, 'python_login/destination.html', context )


def add_trip(request, id):
    # create a new relationship between users
    trip = Trip.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    join = trip.users.add(user)
    return redirect("/travels")


def logout(request):
    # clean session and logout
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')
