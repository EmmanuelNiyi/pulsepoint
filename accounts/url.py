from django.urls import path, re_path

from accounts.views import CreateRoleView, GetAllRolesView, UserListView, ActivateView, UserLoginView, \
    SendActivationCodeView

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
    # path('profile/<int:user>/', UserProfileDetailView.as_view()),

]
