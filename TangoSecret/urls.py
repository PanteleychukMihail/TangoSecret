from django.conf.urls.static import static
from django.contrib import admin
from TangoSecret import settings
from tangoschool.views import *
from django.urls import path, include

admin.site.site_header = "Админка Tango Secret"
admin.site.index_title = "Tango Secret"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tangoschool.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
