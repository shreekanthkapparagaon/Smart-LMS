from django.shortcuts import render,redirect
from users.models import CustomUser

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
    return redirect('home')

def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        print('user not loged in ')
    return redirect('home')
def registerUser(request):
    if request.method =="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        if password != password1:
            # messages.error('password doesnt match....!')
            return redirect('home')
        user = CustomUser.objects.filter(email=email).first()
        if user is not None:
            # messages.error('opss.. user exist...')
            return redirect('home')
        user = CustomUser(email=email)
        user.set_password(password)
        user.save()
        # messages.success('user register successfully....!')
        return redirect('home')
    return redirect('home')