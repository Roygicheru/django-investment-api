from django.urls import path, include
from django.contrib import admin
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
    path('api/', include(router.urls)),
    path(
        'api/user-transactions/',
        UserTransactionsView.as_view(),
        name='user-transactions'
    ),
    path('api-token-auth/', auth_views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/profile/', user_profile, name='user_profile'),
]
