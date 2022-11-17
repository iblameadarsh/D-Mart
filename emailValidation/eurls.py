from django import urls
from django.urls import path
from .views import FormHandler, ViewForm

urlpatterns = [
    path('email-Validation/', FormHandler.as_view(), name='form-submit'),
    path('form-view/<int:pk>', ViewForm.as_view(), name='from-view')

]
