from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from ussrhistory import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nuclearplants.urls')),
    path("__reload__/", include("django_browser_reload.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
