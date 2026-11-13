
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from cart.models import Cart
from .models import Order, OrderItem


@login_required
def checkout(request):

    cart = Cart.objects.get_or_create(
        customer=request.user
    )[0]

    items = cart.items.select_related('product')

    if not items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    if request.method == 'POST':

        shipping_address = request.POST.get(
            'shipping_address', ''
        ).strip()

        if not shipping_address:
            messages.error(
                request,
                "Please enter your delivery address."
            )
            return render(request, 'checkout.html', {
                'items': items,
                'total': total
            })

        with transaction.atomic():

            for item in items:
                if item.quantity > item.product.stock:
                    messages.error(
                        request,
                        f"Insufficient stock for {item.product.name}."
                    )
                    return redirect('cart')

            order = Order.objects.create(
                customer=request.user,
                total_amount=total,
                shipping_address=shipping_address,
                status='pending'
            )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

                item.product.stock -= item.quantity
                item.product.save(update_fields=['stock'])

            cart.items.all().delete()

        return redirect('make_payment', order_id=order.id)

    return render(request, 'checkout.html', {
        'items': items,
        'total': total
    })


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        customer=request.user
    ).prefetch_related(
        'items__product',
        'payments'
    ).order_by('-created_at')

    for order in orders:

        items = list(order.items.all())

        order.can_cancel = (
            order.status == 'pending'
            and bool(items)
            and all(
                item.vendor_status == 'pending'
                for item in items
            )
        )

        for item in items:
            item.subtotal = item.price * item.quantity

    return render(request, 'my_orders.html', {
        'orders': orders
    })


def update_order_status(order):

    items = order.items.all()

    if not items.exists():
        return

    statuses = list(
        items.values_list('vendor_status', flat=True)
    )

    if all(status == 'cancelled' for status in statuses):
        order.status = 'cancelled'

    elif all(status == 'delivered' for status in statuses):
        order.status = 'delivered'

    elif all(
        status in ['shipped', 'delivered']
        for status in statuses
    ):
        order.status = 'shipped'

    elif all(
        status in ['confirmed', 'shipped', 'delivered']
        for status in statuses
    ):
        order.status = 'confirmed'

    else:
        order.status = 'pending'

    order.save(update_fields=['status'])


@login_required
def cancel_order(request, order_id):

    if request.method != 'POST':
        return redirect('my_orders')

    with transaction.atomic():

        order = get_object_or_404(
            Order.objects.select_for_update(),
            id=order_id,
            customer=request.user
        )

        items = list(
            order.items.select_related('product').select_for_update()
        )

        if order.status != 'pending' or not items or not all(
            item.vendor_status == 'pending'
            for item in items
        ):
            messages.error(
                request,
                "This order cannot be cancelled because one or more products have already been processed."
            )
            return redirect('my_orders')

        for item in items:

            item.product.stock += item.quantity
            item.product.save(update_fields=['stock'])

            item.vendor_status = 'cancelled'
            item.save(update_fields=['vendor_status'])

        order.status = 'cancelled'
        order.save(update_fields=['status'])

    messages.success(
        request,
        "Your order has been cancelled successfully!"
    )

    return redirect('my_orders')
