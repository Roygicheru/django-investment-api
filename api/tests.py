from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, InvestmentAccount, InvestmentAccountUser, Transaction


class InvestmentAccountTests(APITestCase):
    def setUp(self):
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

        # Validate investment_account field
        self.assertEqual(
            response.data['investment_account'],
            self.investment_account.pk
        )
        self.assertEqual(response.data['amount'], '100.00')
        self.assertEqual(response.data['date'], '2023-06-08')

    def test_admin_user_transactions(self):
        admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpass'
        )
        url = reverse('user-transactions') + f'?user_id={self.user.id}'
        self.client.force_authenticate(user=admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['transactions']), 1)
        self.assertEqual(response.data['total_balance'], 100)
