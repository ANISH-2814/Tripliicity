from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Basic placeholder URLs - will be implemented later
    path('', views.placeholder_view, name='home'),
]
