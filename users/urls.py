from django.contrib.auth import views
from django.urls import path, reverse_lazy

from .views import SignUp

urlpatterns = [
    path(
        'signup/',
        SignUp.as_view(),
        name='signup'
    ),
    path(
        'password_change/',
        views.PasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        'password_change/done/',
        views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),
    path('password_reset/',
         views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             success_url=reverse_lazy('password_reset_done')
         ),
         name='password_reset'),
    path(
        'password_reset/done/',
        views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'password_reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path('password_reset/complete/',
         views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'
         ),
]
