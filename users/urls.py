from django.conf.urls import url
from django.contrib.auth import views
from django.urls import reverse_lazy

from .views import SignUp

urlpatterns = [
    url(r'^signup/$',
        SignUp.as_view(),
        name='signup'
        ),
    url(r'^password_change/$', views.PasswordChangeView.as_view(), name='password_change'),
    url(r'^password_change/done/$', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    url(r'^password_reset/$',
        views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            success_url=reverse_lazy('password_reset_done')),
        name='password_reset'),
    url(r'^password_reset/done/$', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
        ),
    url(r'^password_reset/complete/$',
        views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
        ),
]
