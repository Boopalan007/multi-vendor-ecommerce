
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.models import Product
from .models import Review
from .forms import ReviewForm


@login_required
def add_review(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    existing_review = Review.objects.filter(
        customer=request.user,
        product=product
    ).first()

    if request.method == 'POST':

        form = ReviewForm(
            request.POST,
            instance=existing_review
        )

        if form.is_valid():

            review = form.save(commit=False)
            review.customer = request.user
            review.product = product
            review.save()

            if existing_review:
                messages.success(
                    request,
                    "Your review has been updated successfully!"
                )
            else:
                messages.success(
                    request,
                    "Your review has been submitted successfully!"
                )

            return redirect('products')

    else:

        form = ReviewForm(instance=existing_review)

    return render(request, 'add_review.html', {
        'form': form,
        'product': product,
        'existing_review': existing_review
    })
