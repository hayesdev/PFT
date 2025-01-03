
import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description, date_format
# import matplotlib as plt
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]

    @classmethod
    def inititalize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            # df == DataFrame
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        # using this context manager Python will automatically close file once done with it
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        # this is accessing all of the values of the "date" column from the CSV
        df["date"] = pd.to_datetime(df["date"], format=date_format)
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date, date_format)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        # returns a filtered df by locating (loc) everything where mask is True
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('No transactinos found in the given date range')
        else:
            print(
                f"Transactions from {start_date.strftime(date_format)} to {end_date.strftime(date_format)}")
            # formatters= takes a formatting function and applies to each item of an iterable (similar to map)
            print(filtered_df.to_string(index=False, formatters={
                  "date": lambda x: x.strftime(date_format)}))

            # looks a litle weird, but using pandas we can find every row in the "category" column
            # that equals Income, then grab the "amount" columns from those rows and sum the values
            total_income = filtered_df[filtered_df["category"]
                                       == "Income"]["amount"].sum()

            total_expense = filtered_df[filtered_df["category"]
                                        == "Expense"]["amount"].sum()
            print("\nSummary:")

            # :.2f is a feature of fstrings that rounds to 2 decimal places
            print(f"Total income: ${total_income:.2f}")
            print(f"Total expense: ${total_expense:.2f}")
            print(f"Net savings: ${(total_income - total_expense):.2f}")

        return filtered_df


def add():
    CSV.inititalize_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or press enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    df.set_index("date", inplace=True)

    income_df = df[df["category"] == "Income"].resample(
        "D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample(
        "D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index,
             expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and sumamry within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting... ")
            break
        else:
            print("Invalid option. Enter 1, 2, or 3.")

            # CSV.get_transactions("01-01-2023", "30-12-2024")

            # CSV.inititalize_csv()
            # CSV.add_entry("20-07-2024", 125.62, "Income", "Salary")


if __name__ == "__main__":
    main()
