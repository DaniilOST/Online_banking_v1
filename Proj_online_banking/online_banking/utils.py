from decimal import Decimal
def get_conversion_rate(from_currency, to_currency):
    return 1.2 

def convert_currency(amount, from_currency, to_currency):
    conversion_rate = get_conversion_rate(from_currency, to_currency)
    if conversion_rate is None:
        raise ValueError("Не удалось получить курс обмена для этих валют.")
    
    conversion_rate = Decimal(conversion_rate)
    
    converted_amount = Decimal(amount) * conversion_rate
    return converted_amount

