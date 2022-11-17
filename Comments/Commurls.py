from django import urls
from django.urls import path, include
from .views import WriteComm, ListComm, CommDel, CommUpdate

urlpatterns = [
    path('list/<int:pk>/comment/', WriteComm.as_view(), name='post'),
    path('comm-del/<int:fk>/<int:pk>', CommDel.as_view(), name='del_com'),
    path('comm-update/<int:pk>', CommUpdate.as_view(), name='update_com'),
    path('comm-list/<int:fk>', ListComm.as_view(), name='list_com'),

   ]
