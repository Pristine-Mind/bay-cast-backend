"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import re_path as url
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers

from product import views as product_views
from user.views import (
    RegistrationView,
    LoginView,
    UserViewSet,
)

router = routers.DefaultRouter()

router.register(r'product', product_views.ProductViewSet, basename='product')
router.register(r'process', product_views.ProcessViewSet, basename='process')
router.register(r'stations', product_views.StationViewSet, basename='station')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r"^api/v1/", include(router.urls)),
    url(r"^register", RegistrationView.as_view()),
    url(r"^login", LoginView.as_view()),
    path('station-product-process/', product_views.StationProductProcessView.as_view(), name='station-product-process')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
