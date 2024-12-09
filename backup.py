# This is a multi-currency exchange calculator

# TO-DO: ask for user inputs
# Which currency do you want to exchange?
# Do you have a specific amount you need in the currency you want to receive? (y/n)
    # y => The amount: ___(in currency you want to receive)
        # Do you have specific bills requirements? (small or large bills) (y/n)
        # n => Default bill: Largest notes comes first.
        # y => What are the bills you need? <add until given amount or shows error if exceeds>
    # n => You want to exchange the currency you have.
        # What currency do you have?
            # Enter currency
            # How much do you have in <that currency>?
            # <Calculate the exchange rate>

supported_currencies = {}
target_c = ""

def main():
    global target_c
    # Ask for currency user want
    target_c = check_currency("Which currency do you want to receive? ")

    # Ask user to choose options
    option = input(f"Would you like to specify the amount you want to receive in {target_c}? (y/n): ").strip().lower()

    if option == "y":
        # Specify the amount user want to recieve
        target_amount = float(input("Specify the amount you want to receive: "))
        # Specify the currency user has
        source_c = check_currency("Which currency are you exchanging from? ")
        # TODO: optimize code
        total = supported_currencies[source_c] * target_amount
        print(f"Pay {total} {source_c} to receive {target_amount:.2f} {target_c}")
        sys.exit(0)
    
    if option == "n":
        # Specify the amount user want to exchange from
        print("You want to exchange from the currency you have./n")
        total = 0.00
        source_money = []
        p = inflect.engine()
        while True:
            try:
                source_c = check_currency("Which currency are you exchanging from? ")
                source_amount = check_amount(f"How much do you want to exchange from {source_c}? ")
                source_money.append(format(source_amount, ".2f")+ " " + source_c)
                total += float(source_amount) / float(supported_currencies[source_c])
                print(f"You receive total {total:.2f} {target_c} from {p.join(source_money)}")
            except EOFError:
                print("")
                sys.exit(0)
    


def exchange_rate(from_c):
    '''
    Calculate exchange rate from source to target currency
    
    :param from_c: Source Currency
    :type from_c: str
    :return: float
    '''
    global supported_currencies
    source_currency = check_currency("Which currency are you exchanging from? ")
    return supported_currencies[from_c], source_currency
   

def check_amount(m):
    '''
    Ask user for the amount they want

    :param m: Message 
    :type m: str
    :return: amount
    :return type: float
    '''
    while True:
        try:
            return float(input(m).strip())
        except ValueError:
            print("Enter decimal numbers only!")
            pass

def check_currency(m):
    '''
    Ask user about currency they want to exchange

    :param m: Message for input
    :param c: Name of currency user wants
    :type c: str
    :return: if the currency is supported, otherwise prompt the question
    '''  
    api_key = dotenv_values(".env")["API_key"]
    while True:
        # Get user input for currency
        c = input(m).strip().upper()
        global supported_currencies
        # Target currency always comes first. If empty, request API call
        if not supported_currencies:
            r = requests.get(f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{c}")
            o = r.json()
            supported_currencies = o["conversion_rates"]
            print('api called here!')
        if c in supported_currencies:
            return c
        else:
            print("Invalid currency, please try again!")
        



if __name__ == "__main__":
    main()