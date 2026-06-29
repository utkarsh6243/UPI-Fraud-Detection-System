import pandas as pd
import numpy as np
import random

np.random.seed(42)

NUM_RECORDS = 50000

banks = [
    "SBI",
    "HDFC",
    "ICICI",
    "Axis",
    "PNB",
    "BOB",
    "Canara",
    "Kotak"
]

locations = [
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Pune",
    "Jaipur",
    "Lucknow",
    "Ahmedabad"
]

devices = [
    "Android",
    "iPhone",
    "Desktop"
]

transaction_types = [
    "Merchant",
    "P2P",
    "Recharge",
    "Bill Payment"
]

rows = []

for _ in range(NUM_RECORDS):

    amount = round(np.random.exponential(3000), 2)

    if amount > 100000:
        amount = 100000

    hour = random.randint(0, 23)

    sender_bank = random.choice(banks)

    receiver_bank = random.choice(banks)

    location = random.choice(locations)

    device = random.choice(devices)

    transaction_type = random.choice(transaction_types)

    account_age = random.randint(1, 120)

    daily_transactions = random.randint(1, 20)

    previous_frauds = random.randint(0, 5)

    new_device = random.randint(0, 1)

    new_location = random.randint(0, 1)

    balance = round(random.uniform(500, 200000), 2)

    fraud = 0

    risk = 0

    if amount > 50000:
        risk += 2

    if previous_frauds > 1:
        risk += 3

    if new_device == 1:
        risk += 1

    if new_location == 1:
        risk += 1

    if hour >= 23 or hour <= 4:
        risk += 1

    if daily_transactions > 15:
        risk += 2

    if balance < amount:
        risk += 2

    if device == "Desktop":
        risk += 1

    if random.random() < risk / 12:
        fraud = 1

    rows.append({

        "amount": amount,

        "balance": balance,

        "hour": hour,

        "sender_bank": sender_bank,

        "receiver_bank": receiver_bank,

        "location": location,

        "device": device,

        "transaction_type": transaction_type,

        "account_age": account_age,

        "daily_transactions": daily_transactions,

        "previous_frauds": previous_frauds,

        "new_device": new_device,

        "new_location": new_location,

        "fraud": fraud

    })

df = pd.DataFrame(rows)

print(df.head())

print()

print(df["fraud"].value_counts())

df.to_csv("upi_fraud_dataset.csv", index=False)

print()

print("Dataset saved as upi_fraud_dataset.csv")