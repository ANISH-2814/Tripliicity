from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/<slug:package_slug>/', views.create_booking, name='create_booking'),
    path('payment-complete/', views.payment_complete, name='payment_complete'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
