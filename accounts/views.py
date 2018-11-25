from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

# Create your views here.

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')

        #user is not logged in
        messages.error(request, 'Invalid credentials')
        return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    #logut user
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')

def register(request):

    if request.method == 'POST':
        # get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_name = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']

        #validate paswword
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        #check username
        if User.objects.filter(username=user_name).exists():
            messages.error(request, 'That username is taken')    
            return redirect('register')
        
        #check email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'That email is being used')    
            return redirect('register')
        
        #save user
        user = User.objects.create_user(username=user_name, password=password1, email=email, first_name=first_name, last_name=last_name)
        user.save()
        messages.success(request, 'You are now registered and can log in')
        return redirect('login')
        #auto login
        #auth.login(request, user)
        #messages.success(request, 'You are not logged in')
        #return redirect('index')
    else:
        return render(request, 'accounts/register.html')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)
