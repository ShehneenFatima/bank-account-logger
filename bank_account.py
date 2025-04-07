import os
import csv
from datetime import datetime
from fpdf import FPDF

# Transaction Logger Decorator
def transaction_logger(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)

        # Format args and kwargs cleanly
        formatted_args = ", ".join(map(str, args)) if args else "No args"
        formatted_kwargs = ", ".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else "No kwargs"

        # Log entry
        log_entry = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Clean timestamp format
            func.__name__.capitalize(),
            formatted_args,
            formatted_kwargs,
            self.balance
        ]

        # Ensure logs/ directory exists
        os.makedirs("logs", exist_ok=True)

        # Define the path for the CSV file specific to the username
        log_path = f"logs/{self.username}_transactions.csv"

        # Check if the CSV file exists, if not, create it and write the header
        file_exists = os.path.exists(log_path)
        try:
            with open(log_path, 'a', newline='') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['Date', 'Transaction', 'Arguments', 'Keyword Arguments', 'Balance'])  # CSV header
                writer.writerow(log_entry)
        except Exception as e:
            print(f"Error writing to log file: {e}")

        return result
    return wrapper

# BankAccount class to manage user accounts and transactions
class BankAccount:
    def __init__(self, username, initial_balance=0):
        self.username = username
        self.balance = initial_balance

    @transaction_logger  # Apply the decorator to log transactions
    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self.balance += amount
        print(f"Deposited {amount}. New balance: {self.balance}")

    @transaction_logger  # Apply the decorator to log transactions
    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > self.balance:
            print("Insufficient funds")
            return
        self.balance -= amount
        print(f"Withdrew {amount}. New balance: {self.balance}")

    def get_balance(self):
        return self.balance

    def generate_pdf(self):
        # Create instance of FPDF class
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Set font
        pdf.set_font("Arial", size=12)

        # Add title
        pdf.cell(200, 10, txt=f"Transactions for {self.username}", ln=True, align='C')
        pdf.ln(10)  # Line break

        # Open the CSV file containing transactions
        log_path = f"logs/{self.username}_transactions.csv"
        try:
            with open(log_path, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)

                # Extract starting balance
                if len(rows) > 1:
                    starting_balance = rows[1][-1]  # Balance from the first transaction
                else:
                    starting_balance = self.balance

                # Add starting balance to PDF
                pdf.cell(200, 10, txt=f"Starting Balance: {starting_balance}", ln=True)
                pdf.ln(10)

                # Add transaction details
                for row in rows[1:]:  # Skip the header row
                    if len(row) == 5:  # Ensure the row has the expected number of columns
                        date, transaction, args, kwargs, balance = row
                        pdf.cell(200, 10, txt=f"{date} - {transaction}: args={args} kwargs={kwargs} balance={balance}", ln=True)
                    else:
                        print(f"Skipping malformed row: {row}")
        except FileNotFoundError:
            print(f"Log file not found: {log_path}")
            return
        except Exception as e:
            print(f"Error reading log file: {e}")
            return

        # Save the PDF to a file
        pdf_output_path = f"logs/{self.username}_transactions.pdf"
        try:
            pdf.output(pdf_output_path)
            print(f"PDF generated: {pdf_output_path}")
        except Exception as e:
            print(f"Error generating PDF: {e}")

# Sample usage
if __name__ == "__main__":
    acc = BankAccount("john_doe", 100)
    acc.deposit(50)
    acc.withdraw(30)
    acc.deposit(100)
    acc.withdraw(60)

    # Generate PDF report
    acc.generate_pdf()

    # Final balance
    print(f"Final balance: {acc.get_balance()}")
