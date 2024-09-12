from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from .models import (
    User,
    InvestmentAccount,
    InvestmentAccountUser,
    Transaction
)


class InvestmentAccountTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.investment_account = InvestmentAccount.objects.create(
            name='Test Account'
        )
        InvestmentAccountUser.objects.create(
            user=self.user,
            investment_account=self.investment_account,
            permission='crud'
        )
        self.transaction = Transaction.objects.create(
            investment_account=self.investment_account,
            amount=100,
            date='2023-06-08'
        )

    def test_retrieve_transactions(self):
        url = reverse('transaction-detail', kwargs={'pk': self.transaction.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.transaction.pk)
        self.assertEqual(
            response.data['investment_account'],
            self.investment_account.pk
        )
        self.assertEqual(response.data['amount'], '100.00')
        self.assertEqual(response.data['date'], '2023-06-08')

    def test_admin_user_transactions(self):
        admin_user = User.objects.create_superuser(
            username='roygicheru',
            password='somethingdifficult'
        )
        url = reverse('user-transactions') + f'?user_id={self.user.id}'

        print(f"Admin User ID: {admin_user.id}")
        print(f"Admin User Is Staff: {admin_user.is_staff}")
        print(f"Admin User Is Superuser: {admin_user.is_superuser}")

        self.client.force_authenticate(user=admin_user)

        print(
            "Is authenticated: "
            f"{self.client.handler._force_user.is_authenticated}"
        )

        response = self.client.get(url, format='json')

        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        print(f"Content: {response.content}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if response.status_code == status.HTTP_200_OK:
            self.assertIn('transactions', response.data)
            self.assertIn('total_balance', response.data)
            self.assertIsInstance(response.data['transactions'], list)
            self.assertIsInstance(
                response.data['total_balance'],
                (int, float, Decimal)
            )

            self.assertEqual(len(response.data['transactions']), 1)
            self.assertEqual(
                Decimal(response.data['total_balance']), Decimal('100'))
        else:
            print("Test failed due to unexpected status code")
