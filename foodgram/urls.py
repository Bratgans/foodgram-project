from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

handler404 = "recipes.views.page_not_found"
handler500 = "recipes.views.server_error"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls'), name='recipes'),
    path('auth/', include('users.urls'), name='login'),
    path('auth/', include('django.contrib.auth.urls')),
    path("author/", views.flatpage, {"url": "author/"},
         name="about_author"),
    path("spec/", views.flatpage, {"url": "spec/"},
         name="about_spec"),
]
