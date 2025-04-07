import os
from datetime import datetime

def transaction_logger(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        log_entry = f"{datetime.now()}: {func.__name__.capitalize()} - args: {args}, kwargs: {kwargs}, balance: {self.balance}\n"
        log_path = f"{self.username}_transactions.log"
        with open(log_path, 'a') as f:
            f.write(log_entry)
        return result
    return wrapper

class BankAccount:
    def __init__(self, username, initial_balance=0):
        self.username = username
        self.balance = initial_balance

    @transaction_logger
    def deposit(self, amount):
        self.balance += amount

    @transaction_logger
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def get_balance(self):
        return self.balance

# Sample usage
if __name__ == "__main__":
    acc = BankAccount("john_doe", 100)
    acc.deposit(50)
    acc.withdraw(30)
    print(f"Final balance: {acc.get_balance()}")
