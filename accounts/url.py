from django.urls import path, re_path

from accounts.views import CreateRoleView, GetAllRolesView

# urlpatterns = [
#     path('invite/', InviteClientView.as_view(), name='invite'),
#
# ]

urlpatterns = [
    path('role/create/', CreateRoleView.as_view()),
    path('role/get/all/', GetAllRolesView.as_view())

]