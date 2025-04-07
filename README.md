# Bank Account Logger

This is a Python class that mimics a bank account. It includes custom decorators to log all transactions to a specific log file for each user.

## Features
- Deposit and withdraw funds
- Track all transactions in a user-specific log file
- Simple implementation of a bank account

## Usage

```python
from bank_account import BankAccount

account = BankAccount("john_doe", 100)
account.deposit(50)
account.withdraw(30)
# bank-account-logger
