from rest_framework import viewsets, permissions, views, response, status
from django.db.models import Sum
from .models import InvestmentAccount, Transaction
from .serializers import InvestmentAccountSerializer, TransactionSerializer
from .permissions import InvestmentAccountPermission


class InvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        InvestmentAccountPermission
    ]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        InvestmentAccountPermission
    ]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(
            investment_account__users=user
        )

        # Ensure correct instance filtering
        if not queryset.exists():
            raise ValueError(
                "No transactions found for the current user."
            )

        return queryset


class UserTransactionsView(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        user_id = request.query_params.get('user_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        queryset = Transaction.objects.filter(
            investment_account__users__id=user_id
        )

        # Validate queryset
        if not queryset.exists():
            return response.Response(
                {'error': 'No transactions found for the given user.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        total_balance = queryset.aggregate(Sum('amount'))['amount__sum'] or 0

        serializer = TransactionSerializer(queryset, many=True)
        data = {
            'transactions': serializer.data,
            'total_balance': total_balance
        }
        return response.Response(data)
