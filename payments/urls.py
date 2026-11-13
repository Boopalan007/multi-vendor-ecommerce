
from django.urls import path
from . import views

urlpatterns = [
    path('<int:order_id>/', views.make_payment, name='make_payment'),
]
