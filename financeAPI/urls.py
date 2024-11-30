from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, include
from rest_framework import routers
from rest_framework.reverse import reverse_lazy
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('social-auth/', include('social_django.urls', namespace='social')),

    path('profile/', ProfileAPI.as_view(), name='profile'),
    path('profile-create/', ProfileCreate.as_view(), name='crt_profile'),
    path('profile-update/<str:username>/', ProfileUpdate.as_view(), name='upd_profile'),

    path('objects/', ObjectAPI.as_view(), name='object'),
    path('object-create', ObjectCreate.as_view(), name='object_create'),
    path('object-update/<slug:object_slug>/', ObjectUpdate.as_view(), name='object_update'),
    path('object-remove/<slug:object_slug>/', ObjectRemove.as_view(), name='object_remove'),

    path('calculate-program/', CalculateInformation.as_view(), name='calculate'),

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
