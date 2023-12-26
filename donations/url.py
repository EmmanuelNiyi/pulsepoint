from django.urls import path, re_path

from donations.views import DonorProfileDetailView, GetAllDonorProfilesView

urlpatterns = [

    path('donor/profile/<int:user>/', DonorProfileDetailView.as_view()),
    path('donor/profile/all/', GetAllDonorProfilesView.as_view()),

]
