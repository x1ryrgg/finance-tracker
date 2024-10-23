from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, include
from rest_framework import routers
from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('profile/', Profile.as_view(), name='profile'),
    path('objects/', ObjectList.as_view(), name='object'),
    path('crt_object', ObjectCreate.as_view(), name='object_create'),
    path('crt_object/<slug:object_slug>/', ObjectUpdate.as_view(), name='object_update'),
    path('rem_object/<int:pk>/', ObjectRem.as_view(), name='object_remove'),

    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('api/auth_user/', include('rest_framework.urls')),

    path('passsword-reset', PasswordResetView.as_view(template_name='reset_password/password_reset_form.html',
                                                      email_template_name='reset_password/password_reset_email.html',
                                                      success_url=reverse_lazy('password_reset_done')),
                                                      name='password_reset'),
    path('passsword-reset/done/', PasswordResetDoneView.as_view(template_name='reset_password/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="reset_password/password_reset_confirm.html",
                                                                    success_url=reverse_lazy('password_reset_complete')),
        name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="reset_password/password_reset_complete.html"),
         name='password_reset_complete')
]
