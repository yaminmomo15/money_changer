from project import (
    is_file_exist,
    get_data,
    calculate_price,
)
import pytest
import os
import datetime
from unittest.mock import patch
import csv


def test_calculate_price():
    assert calculate_price(100.0, 0.7215, 0.007215, True) == (137.22786000013724, 0.728715)


def test_is_file_exist():
    assert is_file_exist("test.csv") == "file created"
    os.remove("test.csv")
    assert is_file_exist("transactions.csv") == "file exist"


def test_get_data():
    time_now = datetime.datetime.now()
    date = time_now.strftime("%Y-%m-%d")
    time = time_now.strftime("%H:%M")
    transactions = []
    is_file_exist("test_csv.csv")
    with open("test_csv.csv", "a") as file:
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
        transactions.append(
                    {
                        "Id": 1,
                        "Cashier": "Susan",
                        "Customer": "Jack",
                        "Date": date,
                        "Time": time,
                        "From": "CAD",
                        "Exchanged": 100.00,
                        "To": "USD",
                        "Received": 70.00,
                        "Rate": "100.00 CAD = 70.00 USD",
                    }
                )
        for _ in transactions:
            writer.writerow(_)
        file.close()
    '''
    test existing id
    '''
    assert get_data("test_csv.csv", "ian", "ava") == (2, date, time, "ian", "ava")
    os.remove("test_csv.csv")
    '''
    test new id
    '''
    is_file_exist("test_csv.csv")
    assert get_data("test_csv.csv") == (1, date, time)
    os.remove("test_csv.csv")