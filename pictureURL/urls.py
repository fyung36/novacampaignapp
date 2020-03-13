from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path
from pictureURL.views import *
from . import views

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path('AllCampaigns/', CampaignView.as_view(), name="campaign_list"),
    path('campaigndetail/<slug:auid>', campaigndetail, name='campaigndetail'),
    path("newcampaign/", Upload_Campaign.as_view(),  name="new_campaign"),
    path("new_directory/", UploadCSV.as_view(),  name="new_directoryg"),
    path('directorydetail/<slug:auid>', directorydetail, name='directorydetail'),
    path("edit/<int:id>/", EditListView.as_view(), name="edit_campaign"),
    path("contactus/", EmailAttachementView.as_view(), name="contactus"),
    path("Delete_Campaign/<int:pk>/", delete_campaign, name="delete_campaign"),
    path("smsform/<slug:id>", Publish.as_view(),  name="textform"),
    path("result/", search, name="search"),
    # path("Calender/", calender, name="calender")


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
