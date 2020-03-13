from django.urls import path

from airtel.views import EnterMsisdn, Airtel, Webairtel
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [

    path('advertapp/', Webairtel.as_view()),
    path('checkinfluencer/', Airtel.as_view()),
    path('enter-msisdn/', EnterMsisdn.as_view(), name='enter_msisdn'),

]