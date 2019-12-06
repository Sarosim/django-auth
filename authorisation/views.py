from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from authorisation.forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    """Return index.html"""
    return render(request, 'index.html')

@login_required
def logout(request):
    """Log the user out""" 
    auth.logout(request)
    messages.success(request, "You have successfully been logged out.")
    return redirect(reverse('index'))

def login(request):
    """Return the LOGIN page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(
                username=request.POST['username'],
                password=request.POST['password']
            )
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully been logged in.")
            else:
                login_form.add_error(None, "Username or Password is incorrect!")
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {"login_form":login_form})

def registration(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()
            # WE also authenticate the user and log them in:
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
            if user:
                auth.login(user = user, request = request)
                messages.success(request, "You have successfully been registered.")
                return redirect(reverse('index'))
            else:
                messages.error(request, "Unable to register")   
    else:
        registration_form = UserRegistrationForm()
    
    return render(request, 'registration.html', {"registration_form": registration_form})
