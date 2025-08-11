from django.shortcuts import render,redirect
from django.contrib.auth import urls
from django.contrib.auth import authenticate, login,logout
# Create your views here.
def loginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page
        else:
            print('error')
            # Handle invalid credentials
            pass
    return redirect('home')

def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        print('user not loged in ')
    return redirect('home')