# money_changer
Calculate multi-currency exchange depending on exchange rate and spread rate.
Generate receipt and save transaction record.


# MoneyChanger50
#### Video Demo: 

#### Description:
### What is it?
MoneyChanger50 is a command line app that calculate multi-currency exchange depending on exchange rate and spread rate.
It generates receipt in PDF format and save transaction records in csv format.

### How it works?
User needs to type in the information about 
- the base currency
- foreign currency
- spread rate
- cashier name
- customer name
- the amount they are going to exchange
Real-time exchange rate will get through free public API from https://v6.exchangerate-api.com.
Calculate the exchange rate considering the spread rate and reply it back to the user.
When user has completed entering the information, the app generates receipt.pdf and add the transaction data including the information user typed in into transactions.csv file.


### Libraries:
- request
- inflect
- csv
- datetime
- fpdf2
- dotenv

### How to run:
```
pip install request inflect csv datetime fpdf2 dotenv
python project.py
```

### Background Idea 
I came up with this idea when I went to a money changer to sell multiple currencies during my travel in Thailand . It took significantly longer time to complete the transaction compared to other customers who made single currency exchange. The cashier has to manually look at the exchange rate, calculate the price and add into total for each currency. So, got an idea of developing an app that get the real-time market rate of the currency and  calculate the exchange rate altogether. It allows cashier to add the spread rate of their company as well.

