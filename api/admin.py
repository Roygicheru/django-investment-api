from django.contrib import admin
from .models import InvestmentAccount, InvestmentAccountUser, Transaction


@admin.register(InvestmentAccount)
class InvestmentAccountAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(InvestmentAccountUser)
class InvestmentAccountUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'investment_account', 'permission')
    list_filter = ('permission',)
    search_fields = ('user__username', 'investment_account__name')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('investment_account', 'amount', 'date')
    list_filter = ('investment_account',)
    search_fields = ('investment_account__name',)
    date_hierarchy = 'date'
