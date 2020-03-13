from django.conf import settings
from django.urls import path
from accounts.views import *


urlpatterns = [
    path('login/', login_page , name="login_page"),
    path('logout/', logout, name='logout'),
    path('New_User/', CreateNewUser.as_view(), name='New_User'),
    path('all_user/', alluser , name='all_user'),
    path('userdetail/<slug:name>',  userdetail, name='userdetail'),
    path('changepassword/<slug:user>', changepassword , name='changepassword'),
 ]