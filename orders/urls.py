
from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),

    path('my-orders/', views.my_orders, name='my_orders'),

    path(
        'cancel/<int:order_id>/',
        views.cancel_order,
        name='cancel_order'
    ),
]
