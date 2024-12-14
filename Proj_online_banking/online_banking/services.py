
from django.db import connection
from .models import Account

def TransferFunds(sender_account_id, recipient_account_id, amount, from_currency, to_currency):
    try:
        sender_account = Account.objects.get(account_id=sender_account_id)
        recipient_account = Account.objects.get(account_id=recipient_account_id)

        # Проверка наличия достаточного баланса на счете отправителя
        if sender_account.account_balance < amount:
            raise ValueError("Недостаточно средств на счете отправителя.")

        with connection.cursor() as cursor:
            cursor.callproc('TransferFunds', [sender_account_id, recipient_account_id, amount, from_currency, to_currency])
            cursor.execute("UPDATE accounts SET account_balance = account_balance - %s WHERE account_id = %s", [amount, sender_account_id])
            cursor.execute("UPDATE accounts SET account_balance = account_balance + %s WHERE account_id = %s", [amount, recipient_account_id])

        return True

    except Exception as e:
        raise ValueError(f"An error occurred while transferring funds: {e}")
