from django.conf import settings
from django.conf.urls.static import static
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

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
