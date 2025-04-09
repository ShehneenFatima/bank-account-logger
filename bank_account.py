import csv
from datetime import datetime
from fpdf import FPDF


def transaction_logger(func):
    """Decorator to log each transaction to a CSV file."""

    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)

        formatted_args = ", ".join(map(str, args)) if args else "No args"
        formatted_kwargs = (
            ", ".join(f"{k}={v}" for k, v in kwargs.items())
            if kwargs else "No kwargs"
        )

        log_entry = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            func.__name__.capitalize(),
            formatted_args,
            formatted_kwargs,
            self.balance,
        ]

        # Create logs directory if it doesn't exist
        from os import makedirs, path

        makedirs("logs", exist_ok=True)
        log_path = f"logs/{self.username}_transactions.csv"
        file_exists = path.exists(log_path)

        try:
            with open(log_path, "a", newline="") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(
                        ["Date", "Transaction", "Arguments",
                         "Keyword Arguments", "Balance"]
                    )
                writer.writerow(log_entry)
        except Exception as e:
            print(f"Error writing to log file: {e}")

        return result

    return wrapper


class BankAccount:
    """Represents a simple bank account."""

    def __init__(self, username, initial_balance=0):
        self.username = username
        self.balance = initial_balance

    @transaction_logger
    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self.balance += amount
        print(f"Deposited {amount}. New balance: {self.balance}")

    @transaction_logger
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
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(
            200, 10,
            txt=f"Transactions for {self.username}",
            ln=True,
            align="C"
        )
        pdf.ln(10)

        log_path = f"logs/{self.username}_transactions.csv"

        try:
            with open(log_path, "r") as f:
                reader = csv.reader(f)
                rows = list(reader)

                if len(rows) > 1:
                    starting_balance = rows[1][-1]
                else:
                    starting_balance = self.balance

                pdf.cell(
                    200, 10,
                    txt=f"Starting Balance: {starting_balance}",
                    ln=True
                )
                pdf.ln(10)

                for row in rows[1:]:
                    if len(row) == 5:
                        date, transaction, args, kwargs, balance = row
                        pdf.cell(
                            200, 10,
                            txt=(
                                f"{date} - {transaction}: "
                                f"args={args} kwargs={kwargs} "
                                f"balance={balance}"
                            ),
                            ln=True,
                        )
                    else:
                        print(f"Skipping malformed row: {row}")
        except FileNotFoundError:
            print(f"Log file not found: {log_path}")
            return
        except Exception as e:
            print(f"Error reading log file: {e}")
            return

        output_path = f"logs/{self.username}_transactions.pdf"
        try:
            pdf.output(output_path)
            print(f"PDF generated: {output_path}")
        except Exception as e:
            print(f"Error generating PDF: {e}")


if __name__ == "__main__":
    account = BankAccount("john_doe")
    account.deposit(50)
    account.withdraw(30)
    account.deposit(100)
    account.withdraw(60)
    account.generate_pdf()
    print(f"Final balance: {account.balance}")
