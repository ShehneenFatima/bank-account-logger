# Bank Account Logger Project

This project is designed to simulate a bank account and log transactions using a decorator. It also generates a PDF report of the transactions.

## Features

- **Deposit and Withdrawal**: Allows you to deposit and withdraw money from a bank account, updating the balance accordingly.
- **Transaction Logger**: A decorator is used to log each deposit and withdrawal transaction, saving the transaction details into a CSV file.
- **Transaction Logging**: The transactions are saved in a CSV file under the `logs` directory. The file is named after the username (e.g., `john_doe_transactions.csv`).
- **PDF Report**: A PDF report of the transactions is generated after each set of transactions. The PDF includes a list of all transactions with a timestamp, operation type, arguments, and the resulting balance.
- **Error Handling**: Proper error handling is implemented for cases like insufficient funds and invalid inputs. Also, it handles issues like file access errors.
- **Modular Design**: The code follows object-oriented principles, with a `BankAccount` class to manage user accounts and transactions.

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/bank-account-logger.git
