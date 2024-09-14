# api/views.py

from django.db.models import Sum
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import InvestmentAccount, Transaction, InvestmentAccountUser
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
        account_id = self.kwargs.get('account_id')

        user_permission = InvestmentAccountUser.objects.filter(
            user=user,
            investment_account_id=account_id
        ).first()

        if not user_permission or user_permission.permission not in ['crud',
                                                                     'view']:
            return Transaction.objects.none()

        return Transaction.objects.filter(investment_account_id=account_id)

    def create(self, request, *args, **kwargs):
        account_id = self.kwargs.get('account_id')
        user_permission = InvestmentAccountUser.objects.filter(
            user=request.user,
            investment_account_id=account_id
        ).first()

        if not user_permission or user_permission.permission not in ['crud',
                                                                     'post']:
            return Response(
                {
                    "detail": "You don't have permission to create"
                              "transactions for this account."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(investment_account_id=account_id)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class UserTransactionsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {"error": "User ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        queryset = Transaction.objects.filter(
            investment_account__users__id=user_id
        )

        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        if not queryset.exists():
            return Response(
                {'error': 'No transactions found for the given user.'},
                status=status.HTTP_404_NOT_FOUND
            )

        total_balance = queryset.aggregate(Sum('amount'))['amount__sum'] or 0

        serializer = TransactionSerializer(queryset, many=True)
        data = {
            'transactions': serializer.data,
            'total_balance': total_balance
        }
        return Response(data)
