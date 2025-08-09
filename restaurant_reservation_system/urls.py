"""
URL configuration for restaurant_reservation_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from restaurant_reservation_system import settings

ADMIN_URLS = [
    path("admin/", admin.site.urls),
]

LOCAL_APPS_URLS = [
    path("api/user/", include("apps.user.urls")),
    path("api/book/", include("apps.reserve.urls")),
]

urlpatterns = ADMIN_URLS + LOCAL_APPS_URLS

if settings.DEBUG:
    urlpatterns.extend(
        [
            # YOUR PATTERNS
            path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
            # Optional UI:
            path(
                "api/docs/swagger/",
                SpectacularSwaggerView.as_view(url_name="schema"),
                name="swagger-ui",
            ),
            path(
                "api/docs/redoc/",
                SpectacularRedocView.as_view(url_name="schema"),
                name="redoc",
            ),
        ]
    )
