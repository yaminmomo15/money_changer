import requests
import inflect
import csv
import datetime
from fpdf import FPDF
from fpdf.enums import TableCellFillMode
from fpdf.fonts import FontFace
from dotenv import dotenv_values


class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", size=12)
        self.cell(190, 10, "Money Changer Ltd", align="C")
        self.ln()
        self.set_line_width(0.3)
        self.set_draw_color(r=0, g=100, b=255)
        self.line(x1=10, y1=20, x2=200, y2=20)
        self.cell(190, 8, "123, Exchange Rd, Cityville, Country", align="C")
        self.ln()
        self.cell(190, 8, "Phone: (123) 456-7890", align="C")
        self.ln()
        self.cell(190, 8, "Website: www.moneychangers.com", align="C")
        self.ln(10)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", size=8)
        self.cell(190, 5, "Thank you for using Money Changers Ltd!", align="C")
        self.ln()
        self.cell(190, 5, "www.moneychangers.com", align="C")
        # Printing page number:
        self.set_y(-15)
        self.cell(0, 15, f"Page {self.page_no()}/{{nb}}", align="R")


def main():
    base_currency_code = (
        input("Please enter the base currency code (e.g., USD, EUR, JPY): ")
        .strip()
        .upper()
    )
    exchange_rates = access_exchange_rates(base_currency_code)
    spread_percentage = float(
        input(
            "Please enter the spread percentage applied by the money changer (e.g., 2 for 2%): "
        ).strip()
    )
    transaction_type = (
        input("Would you like to buy or sell foreign currency? (buy/sell): ")
        .strip()
        .lower()
    )
    # TO-DO: loop for selling foreign currency
    message = calculate_exchange(
        base_currency_code, transaction_type, spread_percentage, **exchange_rates
    )

    # TO-DO: print out receipt
    with open("transactions.csv", "r") as file:
        """
        get last row
        get id, cashier, customer, date, time
        get id related from, to, currencies, rate
        """
        fieldnames = [
            "Id",
            "Cashier",
            "Customer",
            "Date",
            "Time",
            "From",
            "Exchanged",
            "To",
            "Received",
            "Rate",
        ]
        reader = csv.DictReader(file, fieldnames=fieldnames)
        last = list(reader)[-1]
        id = last["Id"]
        cashier = last["Cashier"]
        customer = last["Customer"]
        date = last["Date"]
        time = last["Time"]
        file.seek(0)
        transaction = []
        transaction.append(["From", "Exchanged", "To", "Received", "Rate"])
        for row in reader:
            if row["Id"] == id:
                transaction.append(
                    [
                        row["From"],
                        row["Exchanged"],
                        row["To"],
                        row["Received"],
                        row["Rate"],
                    ]
                )
        file.close()

    pdf = PDF()
    pdf.set_line_width(0.3)
    pdf.set_draw_color(r=0, g=100, b=255)
    pdf.add_page()

    pdf.cell(190, 10, f"Date: {date}", align="L")
    pdf.ln()
    pdf.cell(190, 8, f"Time: {time}", align="L")
    pdf.ln()
    pdf.cell(190, 8, f"Transaction ID: {id}", align="L")
    pdf.ln()
    pdf.cell(190, 8, f"Cashier: {cashier}", align="L")
    pdf.ln()
    pdf.cell(190, 8, f"Customer: {customer}", align="L")
    pdf.ln(15)

    # pdf.set_draw_color(0, 0, 0)
    # line_position_y = 96
    pdf.set_line_width(0.3)
    pdf.set_draw_color(0, 100, 255)
    headings_style = FontFace(emphasis="BOLD", color=255, fill_color=(0, 100, 255))
    with pdf.table(
        borders_layout="NO_HORIZONTAL_LINES",
        col_widths=(20, 45, 20, 45, 60),
        headings_style=headings_style,
        line_height=8,
        text_align=("RIGHT"),
        width=190,
    ) as table:
        for data_row in transaction:
            row = table.row()
            # line_position_y += 8
            for datum in data_row:
                row.cell(datum)

    pdf.ln()
    pdf.multi_cell(190, 10, message, align="L")
    pdf.output("receipt.pdf")


def access_exchange_rates(code):
    api_key = dotenv_values(".env")["API_key"]
    requested_data = requests.get(
        f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{code}"
    )
    object_data = requested_data.json()
    return object_data["conversion_rates"]


def calculate_exchange(base, buy_or_sell, spread, **rates):
    total = 0.0000
    foreign_currencies = []
    p = inflect.engine()
    transactions = []
    is_file_exist("transactions.csv")
    cashier = input("Cashier Name: ").strip().capitalize()
    customer = input("Customer Name: ").strip().capitalize()
    id, date, time = get_data("transactions.csv")
    message = ""
    while True:
        try:
            foreign_currency_code = (
                input(
                    "Please enter the foreign currency code you want to exchange (e.g., USD, EUR, JPY): "
                )
                .strip()
                .upper()
            )
            if not foreign_currency_code in rates:
                print("Invalid foreign currency code, please try again!")
                continue
            amount_to_exchange = float(
                input(
                    f"How much of {foreign_currency_code} do you want to exchange? "
                ).strip()
            )
            foreign_currencies.append(
                # format(amount_to_exchange, ",.2f") + " " + foreign_currency_code
                f"{amount_to_exchange:,.2f} {foreign_currency_code}"
            )
            market_rate = float(rates[foreign_currency_code])
            spread_rate = market_rate * spread / 2.0000 / 100.0000
            foreign = f"{p.join(foreign_currencies)}"
            foreign = foreign.replace(";", ",")
            origin = f"{total:.2f} {base}."

            if buy_or_sell == "sell":
                cost, exchange_rate = calculate_price(
                    amount_to_exchange, market_rate, spread_rate, is_selling=True
                )
                total = total + cost
                message = f"You have sold {foreign} to receive {total:,.2f} {base}."
                transactions.append(
                    {
                        "Id": f"{id:05d}",
                        "Cashier": cashier,
                        "Customer": customer,
                        "Date": date,
                        "Time": time,
                        "From": foreign_currency_code,
                        "Exchanged": f"{amount_to_exchange:,.2f}",
                        "To": base,
                        "Received": f"{total:,.2f}",
                        "Rate": f"1 {foreign_currency_code} = {exchange_rate:,.4f} {base}",
                    }
                )
                continue
            else:
                cost, exchange_rate = calculate_price(
                    amount_to_exchange, market_rate, spread_rate, is_selling=False
                )
                total = total + cost
                message = f"You have paid {total:,.2f} {base} to receive {foreign}."
                print(message)
                transactions.append(
                    {
                        "Id": f"{id:05d}",
                        "Cashier": cashier,
                        "Customer": customer,
                        "Date": date,
                        "Time": time,
                        "From": base,
                        "Exchanged": f"{total:,.2f}",
                        "To": foreign_currency_code,
                        "Received": f"{amount_to_exchange:,.2f}",
                        "Rate": f"1 {base} = {exchange_rate:,.4f} {foreign_currency_code}",
                    }
                )
                continue
        except EOFError:
            print("")
            break

    with open("transactions.csv", "a") as file:
        fieldnames = [
            "Id",
            "Cashier",
            "Customer",
            "Date",
            "Time",
            "From",
            "Exchanged",
            "To",
            "Received",
            "Rate",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for _ in transactions:
            writer.writerow(_)
        file.close()
    print(f"message: {message}")
    return message


def is_file_exist(csv_file):
    try:
        with open(csv_file, "r") as f:
            f.close()
            return "file exist"
    except FileNotFoundError:
        with open(csv_file, "w") as file:
            fieldnames = [
                "Id",
                "Cashier",
                "Customer",
                "Date",
                "Time",
                "From",
                "Exchanged",
                "To",
                "Received",
                "Rate",
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            file.close()
            return "file created"


def get_data(csv_file):
    time_now = datetime.datetime.now()
    date = time_now.strftime("%Y-%m-%d")
    time = time_now.strftime("%H:%M")
    id = "0000"
    with open(csv_file) as f:
        fieldnames = [
            "Id",
            "Cashier",
            "Customer",
            "Date",
            "Time",
            "From",
            "Exchanged",
            "To",
            "Received",
            "Rate",
        ]
        reader = csv.DictReader(f, fieldnames=fieldnames)
        for row in reader:
            id = row["Id"]
        f.close()

    # Increment the last id or initiate as "1"
    if not id == "Id":
        id_int = int(id) + 1
    else:
        id_int = 1

    return id_int, date, time


def calculate_price(amount, market_rate, spread_rate, is_selling):
    if is_selling:
        per_price = market_rate + spread_rate
    else:
        per_price = market_rate - spread_rate
    return amount / per_price, per_price


if __name__ == "__main__":
    main()


