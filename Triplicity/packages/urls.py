from django.urls import path
from . import views

app_name = 'packages'

urlpatterns = [
    path('', views.package_list, name='list'), # name = 'list' - for html
    path('category/<slug:category_slug>/', views.package_list, name='list_by_category'),
    path('<slug:package_slug>/', views.package_detail, name='detail'), 
]
