
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Cart, CartItem
from products.models import Product


@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    if product.stock < 1:
        messages.error(request, "Product is out of stock.")
        return redirect('products')

    cart, created = Cart.objects.get_or_create(
        customer=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.error(request, "Maximum stock reached.")

    return redirect('cart')


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(
        customer=request.user
    )

    items = cart.items.select_related('product')

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    return render(request, 'cart.html', {
        'cart': cart,
        'items': items,
        'total': total
    })


@login_required
@require_POST
def update_cart(request, item_id):

    print("========== UPDATE CART ==========")
    print("Received POST data:", request.POST)

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__customer=request.user
    )

    print("Product:", item.product.name)
    print("Old quantity:", item.quantity)
    print("Available stock:", item.product.stock)

    try:
        quantity = int(request.POST.get('quantity', 0))

        print("New quantity received:", quantity)

        if 1 <= quantity <= item.product.stock:

            item.quantity = quantity
            item.save(update_fields=['quantity'])

            item.refresh_from_db()

            print("Updated quantity in database:", item.quantity)

            messages.success(
                request,
                "Cart quantity updated successfully."
            )

        else:
            print("Invalid quantity.")
            messages.error(request, "Invalid quantity.")

    except (ValueError, TypeError):
        print("Invalid quantity received.")
        messages.error(request, "Please enter a valid quantity.")

    print("=================================")

    return redirect('cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__customer=request.user
    )

    item.delete()

    messages.success(request, "Product removed from cart.")

    return redirect('cart')
