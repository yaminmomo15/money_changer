# MoneyChanger50

## Video Demo:  
[MoneyChanger50](https://youtu.be/Z9FXNhSEpVA?si=q4BlDwGT3Qym2vat)

## Description

### What is it?
MoneyChanger50 is a Python-based command-line application designed to simplify multi-currency exchange processes. It calculates exchange rates dynamically based on the latest market data and incorporates a spread rate defined by the money changer. The app generates professional receipts in PDF format and logs all transaction records in a structured CSV file, making it a reliable tool for money changers or financial institutions.

### Key Features
1. **Real-Time Exchange Rates**: Fetches live exchange rate data from the [ExchangeRate-API](https://v6.exchangerate-api.com)
2. **Dynamic Spread Rates**: Allows customizable profit margins through spread percentage
3. **Multi-Currency Transactions**: Supports exchanging multiple foreign currencies in a single session
4. **Automated Receipts**: Generates detailed PDF receipts with transaction details
5. **Transaction Records**: Saves transactions in CSV format for reporting

### How It Works
1. User inputs:
   - Base currency (e.g., CAD, USD)
   - Foreign currency codes
   - Spread percentage
   - Exchange amount
   - Cashier and customer details
2. App calculates exchange based on live rates and spread
3. Generates PDF receipt and logs transaction
4. Supports multiple transactions per session

## Installation and Usage

### Prerequisites
- Python installed on your system

### Installation
Install the required Python libraries:
```bash
pip install requests inflect fpdf2 python-dotenv
```

### Running the Application
```bash
python project.py
```

### Generated Files
- `receipt.pdf`: Transaction receipt
- `transactions.csv`: Transaction log

## Technical Details

### Libraries Used
- `requests`: API data fetching
- `inflect`: Number-to-word conversion
- `csv`: Data logging
- `datetime`: Transaction timing
- `fpdf2`: PDF generation
- `dotenv`: API key management

## Background and Inspiration
The idea for MoneyChanger50 came from a real-world scenario while traveling in Thailand. Managing multiple-currency exchanges manually was a tedious task for the cashier, who had to calculate each transaction individually. This app eliminates the manual hassle by automating the calculation process, ensuring accuracy and saving time for both the cashier and the customer.

By integrating live exchange rates and providing flexibility with customizable spread percentages, MoneyChanger50 streamlines the workflow of money-changing businesses. It also ensures professionalism through PDF receipts and proper record-keeping, catering to the needs of both small-scale and large-scale operations.

