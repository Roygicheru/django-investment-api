from django.db import models
from django.contrib.auth.models import User


class InvestmentAccount(models.Model):
    users = models.ManyToManyField(User, through='InvestmentAccountUser')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class InvestmentAccountUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment_account = models.ForeignKey(
        InvestmentAccount, on_delete=models.CASCADE
    )
    permission = models.CharField(
        max_length=20,
        choices=[
            ('view', 'View Only'),
            ('crud', 'Full CRUD'),
            ('post', 'Post Only')
        ]
    )

    def __str__(self):
        return f"{self.user.pk} - {self.investment_account.name}"


class Transaction(models.Model):
    investment_account = models.ForeignKey(
        InvestmentAccount, on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.amount} - {self.date}"
