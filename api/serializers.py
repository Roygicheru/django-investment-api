from rest_framework import serializers
from .models import InvestmentAccount, Transaction, InvestmentAccountUser


class InvestmentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentAccount
        fields = ['id', 'name', 'users']


class TransactionSerializer(serializers.ModelSerializer):
    investment_account = serializers.PrimaryKeyRelatedField(
        queryset=InvestmentAccount.objects.all()
    )

    class Meta:
        model = Transaction
        fields = ['id', 'investment_account', 'amount', 'date']

    def validate_investment_account(self, value):
        if not isinstance(value, InvestmentAccount):
            raise serializers.ValidationError(
                "Must be an instance of InvestmentAccount."
            )
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        investment_account = validated_data['investment_account']

        if not InvestmentAccountUser.objects.filter(
            user=user,
            investment_account=investment_account,
            permission__in=['crud', 'post']
        ).exists():
            raise serializers.ValidationError(
                "You don't have permission to create transactions for "
                "this investment account."
            )

        return super().create(validated_data)
