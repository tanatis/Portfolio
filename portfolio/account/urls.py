from django.urls import path

from portfolio.account.views import SignUpView, SignOutView, SignInView, AppUserChangePassword, ProfileDetailsView, \
    ProfileEditView, user_delete, account_history

urlpatterns = [
    path('register/', SignUpView.as_view(), name='signup'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('login/', SignInView.as_view(redirect_authenticated_user=True), name='login'),
    path('change-password/', AppUserChangePassword.as_view(), name='change password'),
    path('<int:pk>/history/', account_history, name='transactions history'),
    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='profile edit'),
    path('profile/<int:pk>/delete/', user_delete, name='delete account'),
]
