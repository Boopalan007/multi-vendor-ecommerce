from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('accounts.urls')),

    path('cart/', include('cart.urls')),

    path('orders/', include('orders.urls')),

    path('vendor/', include('vendors.urls')),

    path('customer/', include('customers.urls')),

    path('payments/', include('payments.urls')),

    path('reviews/', include('reviews.urls')),

    path('', views.home, name='home'),

    path('products/', views.product_list, name='products'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
