
from django.shortcuts import render
from django.db.models import Avg, Case, When, Value, IntegerField
from products.models import Product


def home(request):
    products = Product.objects.filter(
        is_available=True,
        vendor__is_approved=True
    ).annotate(
        average_rating=Avg('reviews__rating')
    ).order_by(
        Case(
            When(name__icontains='headphone', then=Value(1)),
            When(name__icontains='watch', then=Value(2)),
            When(name__icontains='earbud', then=Value(3)),
            When(name__icontains='mouse', then=Value(4)),
            default=Value(5),
            output_field=IntegerField()
        ),
        'id'
    )

    return render(request, 'home.html', {
        'products': products
    })


def product_list(request):
    products = Product.objects.filter(
        is_available=True,
        vendor__is_approved=True
    ).annotate(
        average_rating=Avg('reviews__rating')
    )

    search_query = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')

    if search_query:
        products = products.filter(name__icontains=search_query)

    if selected_category:
        products = products.filter(category=selected_category)

    products = products.order_by('id')

    return render(request, 'products.html', {
        'products': products,
        'selected_category': selected_category
    })
