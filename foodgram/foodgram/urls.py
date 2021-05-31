from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls"), name="signup"),
    path("auth/", include("django.contrib.auth.urls")),
]
