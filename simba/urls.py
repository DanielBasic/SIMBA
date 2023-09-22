from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("accounts.urls")),
    path("search/", include("search.urls")),
    path("groupings/", include("groupings.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("product/", include("product.urls")),
    path("dashboard/", include("dashboard.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)