from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("academy/", include("academy.urls", namespace="academy")),
    path("users/", include("users.urls", namespace="users")),
]
