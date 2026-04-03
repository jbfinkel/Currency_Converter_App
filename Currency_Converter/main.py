import requests

def currency_converter(amount, from_currency, to_currency):
    url = f"https://open.er-api.com/v6/latest/{from_currency}"


    try:
        response = requests.get(url)
        data = response.json()
        conversion_rate = data['rates'][to_currency]
        converted_amount = round(amount * conversion_rate)
        return converted_amount
    except requests.exceptions.RequestException as e:
        print(f"error: {e}")
        return None

amount = float(input("Enter currency amount: "))
from_currency = input("Convert from (e.g. EUR, KRW, GBP): ").upper()
to_currency = input("Convert to (e.g. USD, JPY, CAD): ").upper()

converted_amount = currency_converter(amount, from_currency, to_currency)

if converted_amount is not None:
    print(f"({amount} {from_currency} is equal to {converted_amount} {to_currency})")