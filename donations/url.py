from django.urls import path, re_path

from donations.views import DonorProfileDetailView, GetAllDonorProfilesView, CreateBloodDonationView, \
    BloodDonationDetailView, GetAllUserBloodDonationView

urlpatterns = [

    path('donation/create/', CreateBloodDonationView.as_view()),
    path('donation/get/<int:id>/', BloodDonationDetailView.as_view()),
    path('donation/user/get/all/', GetAllUserBloodDonationView.as_view()),

    path('donor/profile/<int:user>/', DonorProfileDetailView.as_view()),
    path('donor/profile/all/', GetAllDonorProfilesView.as_view()),

]
