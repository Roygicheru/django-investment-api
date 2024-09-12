"""This part dictates the permissions of the different accounts"""

from rest_framework import permissions
from .models import InvestmentAccountUser


class InvestmentAccountPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the object is a Transaction,
        # then use the related investment_account
        investment_account = obj.investment_account if hasattr(
            obj, 'investment_account') else obj

        if request.method in permissions.SAFE_METHODS:
            return InvestmentAccountUser.objects.filter(
                user=request.user,
                investment_account=investment_account,
                permission__in=['view', 'crud']
            ).exists()
        elif request.method == 'POST':
            return InvestmentAccountUser.objects.filter(
                user=request.user,
                investment_account=investment_account,
                permission__in=['crud', 'post']
            ).exists()
        else:
            return InvestmentAccountUser.objects.filter(
                user=request.user,
                investment_account=investment_account,
                permission='crud'
            ).exists()
