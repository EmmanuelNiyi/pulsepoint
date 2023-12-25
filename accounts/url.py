from django.urls import path, re_path

from accounts.views import CreateRoleView, GetAllRolesView, UserListView, ActivateView, UserLoginView, \
    SendActivationCodeView, UserProfileDetailView, DonorProfileDetailView, GetAllUserProfilesView, \
    GetAllDonorProfilesView

# urlpatterns = [
#     path('invite/', InviteClientView.as_view(), name='invite'),
#
# ]

urlpatterns = [
    path('role/create/', CreateRoleView.as_view()),
    path('role/get/all/', GetAllRolesView.as_view()),

    path('register/', UserListView.as_view()),
    path('activate/<id>/', ActivateView.as_view()),
    path('send/code/', SendActivationCodeView.as_view()),
    path('login/', UserLoginView.as_view()),
    # path('profile/', UserProfileView.as_view()),
    path('user/profile/<int:user>/', UserProfileDetailView.as_view()),
    path('user/profile/all/', GetAllUserProfilesView.as_view()),
    path('donor/profile/<int:user>/', DonorProfileDetailView.as_view()),
    path('donor/profile/all/', GetAllDonorProfilesView.as_view()),
]
