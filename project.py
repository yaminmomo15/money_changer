import sys
import requests
import json
import inflect
from dotenv import dotenv_values

def main():
    base_currency_code = input("Please enter the base currency code (e.g., USD, EUR, JPY): ").strip().upper()
    exchange_rates = access_exchange_rates(base_currency_code)
    spread_percentage = float(input("Please enter the spread percentage applied by the money changer (e.g., 2 for 2%): ").strip())
    transaction_type = input("Would you like to buy or sell foreign currency? (buy/sell): ").strip().lower()

    # TO-DO: loop for selling foreign currency
    total, currencies = calculate_total(base_currency_code, transaction_type, spread_percentage, **exchange_rates)    

    # TO-DO: transaction_date: get today's date
    personal_details = input("Please provide your full name: ").strip()
    transaction_method = input("How would you like to complete the transaction? (eg. bank transfer, cash, digital wallet): ").strip().capitalize()

    # TO-DO: print out receipt
    

def access_exchange_rates(code):
    api_key = dotenv_values(".env")["API_key"]
    requested_data = requests.get(f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{code}")
    object_data = requested_data.json()
    return object_data["conversion_rates"]

def calculate_total(base, buy_or_sell, spread, **rates):
    # TO-DO: get exchange rate
    print('here!')    
    total = 0.0000
    foreign_currencies = []
    p = inflect.engine()
    while True:
        try:
            foreign_currency_code = input("Please enter the foreign currency code you want to exchange (e.g., USD, EUR, JPY): ").strip().upper()
            if not foreign_currency_code in rates:
                print("Invalid foreign currency code, please try again!")
                pass
            amount_to_exchange = float(input("How much of the foreign currency do you want to exchange? ").strip())
            foreign_currencies.append(format(amount_to_exchange,".2f") + " " + foreign_currency_code)
            market_rate = float(rates[foreign_currency_code])
            spread_rate = market_rate * spread / 2.0000 / 100.0000
            if buy_or_sell == "sell":               
                # total += amount_to_exchange / (market_rate + spread_rate)
                total += calculate_price(amount_to_exchange, market_rate, spread_rate, is_selling=True)
                print(f"You have sold {p.join(foreign_currencies)} to receive {total:.2f} {base}.")
                continue
            else:
                # total = amount_to_exchange / (market_rate - spread_rate)
                total = calculate_price(amount_to_exchange, market_rate, spread_rate, is_selling=False)
                print(f"You have paid {total:.2f} {base} to receive {p.join(foreign_currencies)}.")
                break
        except EOFError:
            print("")
            break        
    return total, foreign_currencies

def calculate_price(amount, market_rate, spread_rate, is_selling):
    if is_selling:
        return amount / (market_rate + spread_rate)
    else:
        return amount / (market_rate - spread_rate)

if __name__ == "__main__":
    main()

# https://www.reddit.com/r/learnpython/comments/1azumnf/how_to_mock_a_dictionary_during_unit_testing_with/