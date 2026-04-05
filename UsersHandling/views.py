from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, CustomerProfile, RestaurantStaff
from .services import create_customer_user

# Create your views here.

def auth(request):
    return render(request, 'UsersHandling/auth.html')


def signup_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        image = request.FILES.get("image")

        if not username or not password or not email:
            messages.error(request, "All fields are required")
            return redirect("auth")

        try:
            create_customer_user(
                username=username,
                email=email,
                password=password,
                dob=dob,
                gender=gender,
                image=image
            )

            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")

        except ValueError as e:
            messages.error(request, str(e))
            return redirect("auth")

        except Exception:
            messages.error(request, "Something went wrong")
            return redirect("auth")

    return redirect("home")



# -------------------------
# 2) LOGIN USER
# -------------------------
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        print(User.objects.filter(username=username).exists())

        if request.user.is_authenticated:
             logout(request)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("I am here")
            return redirect("home")  
        else:
            messages.error(request, "Invalid username or password")
            

            return redirect("auth")

    return redirect("home")


def logout_user(request):
    if request.method != "POST":
        return auth(request)
    if request.user.is_authenticated:
        print(logout(request))
        print("Hello World"*10)
    else:
        print("Bello World -"*10)
 
    return redirect("home")