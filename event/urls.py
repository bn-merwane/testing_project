from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('nooneknow/', admin.site.urls),
    path('',include('client.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
