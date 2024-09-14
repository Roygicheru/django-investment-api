from rest_framework import serializers
from django.utils import timezone
from .models import InvestmentAccount, Transaction, InvestmentAccountUser


class InvestmentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentAccount
        fields = ['id', 'name', 'users']


class TransactionSerializer(serializers.ModelSerializer):
    investment_account = serializers.PrimaryKeyRelatedField(
        queryset=InvestmentAccount.objects.all(),
        required=False
    )

    class Meta:
        model = Transaction
        fields = ['id', 'investment_account', 'amount', 'description', 'date']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if 'date' not in attrs:
            attrs['date'] = timezone.now().date()
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        investment_account = validated_data.get('investment_account')
        if not investment_account:
            account_id = self.context['view'].kwargs.get('account_id')
            if account_id:
                try:
                    investment_account = InvestmentAccount.objects.get(
                        id=account_id)
                    validated_data['investment_account'] = investment_account
                except InvestmentAccount.DoesNotExist:
                    raise serializers.ValidationError(
                        "Invalid investment account ID.")
            else:
                raise serializers.ValidationError(
                    "Investment account is required.")

        if not InvestmentAccountUser.objects.filter(
            user=user,
            investment_account=investment_account,
            permission__in=['crud', 'post']
        ).exists():
            raise serializers.ValidationError(
                "You don't have permission to create"
                " transactions for this investment account."
            )

        return super().create(validated_data)


class InvestmentAccountUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentAccountUser
        fields = ['id', 'user', 'investment_account', 'permission']
