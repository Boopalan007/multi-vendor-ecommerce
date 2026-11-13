
from django.urls import path
from . import views

urlpatterns = [

    path(
        'register/',
        views.vendor_register,
        name='vendor_register'
    ),

    path(
        'dashboard/',
        views.vendor_dashboard,
        name='vendor_dashboard'
    ),

    path(
        'add-product/',
        views.add_product,
        name='add_product'
    ),

    path(
        'edit-product/<int:product_id>/',
        views.edit_product,
        name='edit_product'
    ),

    path(
        'delete-product/<int:product_id>/',
        views.delete_product,
        name='delete_product'
    ),

    path(
        'orders/',
        views.vendor_orders,
        name='vendor_orders'
    ),

    path(
        'update-order/<int:item_id>/',
        views.update_vendor_order_status,
        name='update_vendor_order_status'
    ),

]
