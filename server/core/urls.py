from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("app.urls")),
    path('cart/', include("cart.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC ROOT)