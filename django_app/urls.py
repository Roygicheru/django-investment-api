"""
URL configuration for django_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from api.views import (
    InvestmentAccountViewSet,
    TransactionViewSet,
    UserTransactionsView
)

router = DefaultRouter()
router.register(r'investment-accounts', InvestmentAccountViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path(
        'admin/user-transactions/',
        UserTransactionsView.as_view(),
        name='user-transactions'
    ),
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
