
from django.contrib import admin
from .models import GroupClient, Client, Account, Transaction, Credit, Employee, BalanceHistory, CreditHistory

@admin.register(GroupClient)
class GroupClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name')
    search_fields = ('group_name',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'client_email', 'client_phone', 'client_address')
    search_fields = ('client_name', 'client_email', 'client_phone')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'client', 'account_number', 'account_balance', 'account_status')
    search_fields = ('account_number', 'client__client_name')
    list_filter = ('account_status',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'transaction_amount', 'transaction_type', 'transaction_date')
    search_fields = ('account__account_number', 'transaction_type')
    list_filter = ('transaction_type', 'transaction_date')

@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'credit_amount', 'credit_rate', 'credit_status', 'start_date', 'end_date')
    search_fields = ('client__client_name', 'credit_amount')
    list_filter = ('credit_rate', 'credit_status')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee_name', 'employee_email', 'employee_position')
    search_fields = ('employee_name', 'employee_position', 'employee_email')

@admin.register(BalanceHistory)
class BalanceHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'balance_amount', 'balance_date')
    search_fields = ('account__account_number',)
    list_filter = ('balance_date',)

@admin.register(CreditHistory)
class CreditHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'credit', 'payment_amount', 'history_date')
    search_fields = ('credit__id',)
    list_filter = ('history_date',)
    