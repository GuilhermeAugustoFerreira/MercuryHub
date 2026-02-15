"""
URL configuration for MercuryHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Classification.views import (
    ClassHeaderViewSet,
    CharacteristicViewSet,
    CharacteristicValueViewSet,
    ClassCharacteristicViewSet,
    ClassHeaderDetailView,
    ClassCharacteristicBulkLinkView,
    ClassAvailableCharacteristicsView,
    ClassCharacteristicAddView
)
from Governance.views import MaterialCreationRequestCreateView, MaterialCreationRequestSubmitView

router = DefaultRouter()
router.register(r'classes', ClassHeaderViewSet, basename='classheader')
router.register(r'characteristics', CharacteristicViewSet, basename='characteristic')
router.register(r'characteristic-values', CharacteristicValueViewSet, basename='charactervalue')
router.register(r'class-characteristics', ClassCharacteristicViewSet, basename='classcharacteristic')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/class-details/<str:internal_class_number>/', ClassHeaderDetailView.as_view(), name='class-detail'),
    path('api/class-link-bulk/', ClassCharacteristicBulkLinkView.as_view(), name='class-link-bulk'),
    path(
        'api/class-available-characteristics/<str:internal_class_number>/',
        ClassAvailableCharacteristicsView.as_view(),
        name='class-available-characteristics'
    ),
    path('api/class-characteristics-add/', ClassCharacteristicAddView.as_view(), name='class-characteristics-add'),
    path('api/material-requests/', MaterialCreationRequestCreateView.as_view(), name='material-request-create'),
    path('api/material-requests/<int:request_id>/submit/', MaterialCreationRequestSubmitView.as_view(), name='material-request-submit'),
    path('api/', include(router.urls)),
]
