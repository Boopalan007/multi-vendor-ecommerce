
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import CustomerRegistrationForm
from customers.models import Customer


def register(request):

    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'customer'
            user.save()

            Customer.objects.create(user=user)

            messages.success(
                request,
                'Registration successful!'
            )

            return redirect('home')

    else:
        form = CustomerRegistrationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Vendor login
            if user.role == 'vendor':
                return redirect('vendor_dashboard')

            # Customer login
            return redirect('home')

        else:
            messages.error(request, 'Invalid username or password.')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):

    logout(request)
    return redirect('home')
