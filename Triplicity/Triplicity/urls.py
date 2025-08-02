from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # This will make accounts the default
    path('accounts/', include('accounts.urls')),
    path('packages/', include('packages.urls'))
    # Other app URLs will be added later
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
