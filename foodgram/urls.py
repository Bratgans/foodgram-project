from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views

urlpatterns = [
    path('auth/', include('users.urls'), name='login'),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
    path("author/", views.flatpage, {"url": "author/"},
         name="about_author"),
    path("spec/", views.flatpage, {"url": "spec/"},
         name="about_spec"),
    path('', include('recipes.urls')),
]
