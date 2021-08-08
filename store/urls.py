
from app import urls
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.urls.conf import include
from django.conf import settings


urlpatterns = [
    path('',include('app.urls')),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
