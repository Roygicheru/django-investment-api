from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.authtoken import views as auth_views
from rest_framework.routers import DefaultRouter

from api.views import (
    InvestmentAccountViewSet,
    TransactionViewSet,
    UserTransactionsView
)
from .views_2 import user_profile

router = DefaultRouter()
router.register(r'investment-accounts', InvestmentAccountViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/', include(router.urls)),
    path(
        'api/investment-accounts/<int:account_id>/transactions/',
        TransactionViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='account-transactions'
    ),
    path(
        'user-transactions/',
        UserTransactionsView.as_view(),
        name='user-transactions'
    ),
    path(
        'api/user-transactions/',
        UserTransactionsView.as_view(),
        name='user-transactions'
    ),
    path(
        'admin/transactions/',
        UserTransactionsView.as_view(),
        name='admin-transactions'
    ),
    path(
        'api/investment-accounts/<int:account_id>/transactions/<int:pk>/',
        TransactionViewSet.as_view({
            'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
            'delete': 'destroy'}),
        name='account-transaction-detail'
    ),
    path('api-token-auth/', auth_views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/profile/', user_profile, name='user_profile'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
