from django.urls import path
from BuyNow import views
from BuyNow.views import ProUpdate

urlpatterns = [
    path('', views.Read.as_view(), name='home'),
    path('create-list/', views.Write.as_view(), name='Product'),
    path('list/<int:pk>/', views.ProDetail.as_view(), name='List'),
    path('list-edit/<int:pk>', ProUpdate.as_view(), name='update'),
    path('delete/<int:pk>', views.DeletePro.as_view(), name='delete'),

]
