"""scannerr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from airtel.views import *
from django.conf.urls.static import static
from pictureURL.views import campaign

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('campaign/<slug:auid>', campaign, name='campaign_banner'),
    path('', include('accounts.urls')),
    path('', include('pictureURL.urls')),
    path('', include('airtel.urls')),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
