from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Travelplans
import bcrypt
from django.db.models import Q


# Create your views here.

def landing_page(request):
    return render(request,'landing.html')

def main(request):

    return render(request, 'main.html')

def register_user(request):
    request.POST
    errorsFromValidator = User.objects.userValidator(request.POST)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value, extra_tags= "register")
        return redirect("/main")

    password = request.POST['reg_pw']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print("password hash below")
    print(pw_hash)
    newUser = User.objects.create(name = request.POST['name'], username = request.POST['reg_username'], password = pw_hash, confirm_password = pw_hash)
    print(request.POST)
    print(newUser)
    request.session['loggedinId'] = newUser.id
    return redirect('/user_page')

def user_page(request):
    if 'loggedinId' not in request.session:
        return redirect('main')
    loggedinUser = User.objects.get(id = request.session['loggedinId'])
    context = {
        "loggedinUser": loggedinUser,
        "schedule": Travelplans.objects.filter(Q(uploader = loggedinUser) | Q(favorite = loggedinUser)),
        "not_scheduled": Travelplans.objects.exclude(Q(uploader = loggedinUser) | Q(favorite = loggedinUser))
    }
    return render(request, "user_page.html", context)


def user_login(request):
    request.POST
    errorsFromValidator = User.objects.loginValidator(request.POST)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value, extra_tags= "login")
        return redirect("/main")

    user = User.objects.get(username = request.POST['username'])
    request.session['loggedinId'] = user.id
    print('Login Successful')
    return redirect ('/user_page')

def renderAdd(request):

    return render(request,'add_trip.html')


def postTravel(request):
    request.POST
    errorsFromValidator = Travelplans.objects.tripValidator(request.POST)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value, extra_tags= "trip")
        print('failed upload')
        return redirect("/user_page/add")

    loggedinUser = User.objects.get(id= request.session['loggedinId'])
    newTrip = Travelplans.objects.create(destination = request.POST['destination'], description = request.POST['description'], uploader = loggedinUser, travel_start = request.POST['travel_from'], travel_end = request.POST['travel_to'])
    print(request.POST)
    print(newTrip)
    
    return redirect('/user_page')

def addDestination(request, tripId):
    loggedinUser = User.objects.get(id=request.session['loggedinId'])
    trip = Travelplans.objects.get(id = tripId)
    trip.favorite.add(loggedinUser)
    return redirect('/user_page')

def viewTrip(request, tripId):
    context = {
        "displayTrip": Travelplans.objects.get(id=tripId)
    }
    return render(request, "view.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')