from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# JWT
from rest_framework_simplejwt.views import TokenRefreshView
from Auth.token_serializer import EmailTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# drf-spectacular
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # App Routes
    path("api/", include("API.urls")),
    path("auth/", include("Auth.urls")),
    # JWT Endpoints
    path(
        "auth/token/",
        TokenObtainPairView.as_view(serializer_class=EmailTokenObtainPairSerializer),
        name="token_obtain_pair",
    ),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # OpenAPI Schema & Docs
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
