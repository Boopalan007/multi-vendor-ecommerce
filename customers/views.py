
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Customer


@login_required
def customer_profile(request):

    customer, created = Customer.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        request.user.first_name = request.POST.get(
            'first_name', ''
        ).strip()

        request.user.last_name = request.POST.get(
            'last_name', ''
        ).strip()

        request.user.email = request.POST.get(
            'email', ''
        ).strip()

        request.user.save()

        customer.phone = request.POST.get(
            'phone', ''
        ).strip()

        customer.address = request.POST.get(
            'address', ''
        ).strip()

        customer.city = request.POST.get(
            'city', ''
        ).strip()

        customer.save()

        messages.success(
            request,
            "Profile updated successfully!"
        )

        return redirect('customer_profile')

    return render(request, 'customer_profile.html', {
        'customer': customer
    })
