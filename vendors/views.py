
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Vendor
from .forms import ProductForm, VendorRegistrationForm
from products.models import Product
from orders.models import OrderItem
from orders.views import update_order_status


def vendor_register(request):

    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            Vendor.objects.create(
                user=user,
                business_name=form.cleaned_data['business_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                description=form.cleaned_data['description'],
                is_approved=True
            )

            messages.success(
                request,
                "Vendor registration successful! You can now log in."
            )

            return redirect('login')

    else:
        form = VendorRegistrationForm()

    return render(request, 'vendor_register.html', {
        'form': form
    })


@login_required
def vendor_dashboard(request):

    if request.user.role != 'vendor':
        messages.error(request, "Access denied. Vendors only.")
        return redirect('home')

    vendor = get_object_or_404(Vendor, user=request.user)

    products = vendor.products.all().order_by('-created_at')

    return render(request, 'vendor_dashboard.html', {
        'vendor': vendor,
        'products': products
    })


@login_required
def add_product(request):

    if request.user.role != 'vendor':
        messages.error(request, "Access denied. Vendors only.")
        return redirect('home')

    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor
            product.is_available = True
            product.save()

            messages.success(request, "Product added successfully!")
            return redirect('vendor_dashboard')

    else:
        form = ProductForm()

    return render(request, 'add_product.html', {
        'form': form
    })


@login_required
def edit_product(request, product_id):

    if request.user.role != 'vendor':
        messages.error(request, "Access denied. Vendors only.")
        return redirect('home')

    vendor = get_object_or_404(Vendor, user=request.user)

    product = get_object_or_404(
        vendor.products,
        id=product_id
    )

    if request.method == 'POST':
        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('vendor_dashboard')

    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {
        'form': form,
        'product': product
    })


@login_required
@require_POST
def delete_product(request, product_id):

    if request.user.role != 'vendor':
        messages.error(request, "Access denied. Vendors only.")
        return redirect('home')

    vendor = get_object_or_404(Vendor, user=request.user)

    product = get_object_or_404(
        vendor.products,
        id=product_id
    )

    product.delete()

    messages.success(request, "Product deleted successfully!")
    return redirect('vendor_dashboard')


@login_required
def vendor_orders(request):

    if request.user.role != 'vendor':
        messages.error(request, "Access denied. Vendors only.")
        return redirect('home')

    vendor = get_object_or_404(Vendor, user=request.user)

    order_items = OrderItem.objects.filter(
        product__vendor=vendor
    ).select_related(
        'order',
        'order__customer',
        'product'
    ).order_by('-order__created_at')

    return render(request, 'vendor_orders.html', {
        'order_items': order_items
    })


@login_required
@require_POST
def update_vendor_order_status(request, item_id):

    if request.user.role != 'vendor':
        messages.error(request, "Access denied. Vendors only.")
        return redirect('home')

    vendor = get_object_or_404(
        Vendor,
        user=request.user
    )

    order_item = get_object_or_404(
        OrderItem,
        id=item_id,
        product__vendor=vendor
    )

    new_status = request.POST.get('vendor_status')

    allowed_statuses = [
        'pending',
        'confirmed',
        'shipped',
        'delivered',
        'cancelled'
    ]

    if new_status not in allowed_statuses:
        messages.error(request, "Invalid order status.")
        return redirect('vendor_orders')

    order_item.vendor_status = new_status

    order_item.save(update_fields=['vendor_status'])

    update_order_status(order_item.order)

    messages.success(
        request,
        "Order status updated successfully!"
    )

    return redirect('vendor_orders')
