from django.db import models
from django.contrib.auth.models import User 

class GroupClient(models.Model):
    group_name = models.CharField(max_length=50)

    def __str__(self):
        return self.group_name


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField(unique=True)
    client_phone = models.CharField(max_length=20, blank=True, null=True)
    client_address = models.TextField(blank=True, null=True)
    client_group = models.ForeignKey(GroupClient, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.client_name

    
class Currency(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Account(models.Model):
    id = models.AutoField(primary_key=True, default=1)  
    STATUS_CHOICES = [
        ('Активный', 'Активный'),
        ('Закрытый', 'Закрытый'),
    ]
    
    ACCOUNT_TYPE_CHOICES = [
        ('Текущий', 'Текущий'),
        ('Сберегательный', 'Сберегательный'),
        ('Депозитный', 'Депозитный'),
        ('Валютный', 'Валютный'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=20, unique=True)
    account_number = models.CharField(max_length=20, unique=True)
    account_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    account_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Активный')
    account_type = models.CharField(max_length=15, choices=ACCOUNT_TYPE_CHOICES, default='Текущий')
    currencies = models.ManyToManyField(Currency, related_name='accounts')

    def __str__(self):
        return self.account_number



class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('Пополнение', 'Пополнение'),
        ('Снятие', 'Снятие'),
        ('Перевод', 'Перевод'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)

    def __str__(self):
        return f'{self.transaction_type} - {self.transaction_amount}'

class Credit(models.Model):
    STATUS_CHOICES = [
        ('Активный', 'Активный'),
        ('Закрытый', 'Закрытый'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    credit_amount = models.DecimalField(max_digits=15, decimal_places=2)
    credit_rate = models.DecimalField(max_digits=5, decimal_places=2)
    credit_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Активный')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'Credit #{self.id} for {self.client.client_name}'

class Employee(models.Model):
    employee_name = models.CharField(max_length=100)
    employee_email = models.EmailField(unique=True)
    employee_phone = models.CharField(max_length=20, blank=True, null=True)
    employee_position = models.CharField(max_length=50)

    def __str__(self):
        return self.employee_name

class BalanceHistory(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    balance_date = models.DateField()
    balance_amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'{self.account.account_number} - {self.balance_date}'

class CreditHistory(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
    history_date = models.DateField()
    payment_amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'{self.credit.id} - {self.history_date}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

