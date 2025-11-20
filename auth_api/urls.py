from django.urls import path

from .views import (RegistrationView, LoginView, DeleteAccountView, 
                    UpdateAccountView, ChangePasswordView, AdminUpdateUserView)

urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path("delete/", DeleteAccountView.as_view()),
    path("update/", UpdateAccountView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
    path("admin/update-user/<int:pk>/", AdminUpdateUserView.as_view(), name="admin-update-user"),
    # path('logout/', include('auth.urls')),
]