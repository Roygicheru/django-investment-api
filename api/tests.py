# api/tests.py

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from .models import User, InvestmentAccount, InvestmentAccountUser, Transaction


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
        self.transaction = Transaction.objects.create(
            investment_account=self.investment_account,
            amount=100,
            date='2023-06-08'
        )

    def test_retrieve_transactions_with_crud_permission(self):
        InvestmentAccountUser.objects.create(
            user=self.user,
            investment_account=self.investment_account,
            permission='crud'
        )
        url = reverse(
            'account-transactions',
            kwargs={'account_id': self.investment_account.id}
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.transaction.pk)
        self.assertEqual(
            response.data[0]['investment_account'],
            self.investment_account.pk
        )
        self.assertEqual(response.data[0]['amount'], '100.00')
        self.assertEqual(response.data[0]['date'], '2023-06-08')

    def test_retrieve_transactions_with_view_permission(self):
        InvestmentAccountUser.objects.create(
            user=self.user,
            investment_account=self.investment_account,
            permission='view'
        )
        url = reverse(
            'account-transactions',
            kwargs={'account_id': self.investment_account.id}
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_transactions_with_post_permission(self):
        InvestmentAccountUser.objects.create(
            user=self.user,
            investment_account=self.investment_account,
            permission='post'
        )
        url = reverse(
            'account-transactions',
            kwargs={'account_id': self.investment_account.id}
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_transaction_with_crud_permission(self):
        InvestmentAccountUser.objects.create(
            user=self.user,
            investment_account=self.investment_account,
            permission='crud'
        )
        url = reverse(
            'account-transactions',
            kwargs={'account_id': self.investment_account.id}
        )
        self.client.force_authenticate(user=self.user)
        data = {'amount': 200, 'date': '2023-06-09'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 2)

    def test_create_transaction_with_post_permission(self):
        InvestmentAccountUser.objects.create(
            user=self.user,
            investment_account=self.investment_account,
            permission='post'
        )
        url = reverse(
            'account-transactions',
            kwargs={'account_id': self.investment_account.id}
        )
        self.client.force_authenticate(user=self.user)
        data = {'amount': 200, 'date': '2023-06-09'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 2)

    def test_create_transaction_with_view_permission(self):
        InvestmentAccountUser.objects.create(
            user=self.user,
            investment_account=self.investment_account,
            permission='view'
        )
        url = reverse(
            'account-transactions',
            kwargs={'account_id': self.investment_account.id}
        )
        self.client.force_authenticate(user=self.user)
        data = {'amount': 200, 'date': '2023-06-09'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_admin_user_transactions(self):
        admin_user = User.objects.create_superuser(
            username='roygicheru',
            password='somethingdifficult'
        )
        InvestmentAccountUser.objects.create(
            user=self.user,
            investment_account=self.investment_account,
            permission='crud'
        )
        url = reverse('user-transactions') + f'?user_id={self.user.id}'

        self.client.force_authenticate(user=admin_user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('transactions', response.data)
        self.assertIn('total_balance', response.data)
        self.assertIsInstance(response.data['transactions'], list)
        self.assertIsInstance(
            response.data['total_balance'],
            (int, float, Decimal)
        )
        self.assertEqual(len(response.data['transactions']), 1)
        self.assertEqual(Decimal(response.data['total_balance']),
                         Decimal('100'))
