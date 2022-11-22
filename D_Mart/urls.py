"""D_Mart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from BuyNow import urls
from Comments import Commurls
from django.conf import settings
from django.conf.urls.static import static
from Users.views import WeLogin, Signup
from django.contrib.auth.views import LogoutView
from emailValidation import eurls
# from Users.views import Signup
# from django.views.generic.base import TemplateView


urlpatterns = [
    path('', include(urls)),
    path('', include(Commurls)),
    path('tools/', include(eurls)),
    path('admin/', admin.site.urls),
    path('login/', WeLogin.as_view(), name='login'),
    path('log-out', LogoutView.as_view(next_page='login'), name='logout'),
    path('Sign-up/', Signup.as_view(), name='register'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'D-Mart Admin'
