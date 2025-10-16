from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Home view
def home(request):
    return JsonResponse({
        "message": "Welcome to Country API",
        "docs": {
            "swagger": "/swagger/",
            "redoc": "/redoc/"
        },
        "api": "/api/countries/"
    })


# Swagger schema
schema_view = get_schema_view(
    openapi.Info(
        title="Country API",
        default_version="v1",
        description="Davlatlar haqidagi API hujjatlari",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("countries.urls")),  #  countries app urls ulanadi

    # Swagger & Redoc
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
