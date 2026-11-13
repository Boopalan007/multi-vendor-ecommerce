
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from orders.models import Order
from .models import Payment


@login_required
def make_payment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    if request.method == 'POST':

        payment_method = request.POST.get('payment_method')

        if payment_method not in ['upi', 'card', 'cod']:
            messages.error(request, "Please select a valid payment method.")
            return redirect('make_payment', order_id=order.id)

        payment = Payment.objects.create(
            order=order,
            amount=order.total_amount,
            payment_method=payment_method,
            status='pending'
        )

        if payment_method == 'cod':
            messages.success(request, "Cash on Delivery selected successfully!")
        else:
            messages.success(request, "Demo payment record created. No money was charged.")

        return render(request, 'payment_success.html', {
            'payment': payment
        })

    return render(request, 'payment.html', {
        'order': order
    })
