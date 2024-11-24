# GENERATING EACH DAY IN TEXT DOCUMENT SO THAT WE CAN COPY AND USE IT 
# FOR FUTURE REFERENCES

from datetime import datetime, timedelta

START_YEAR = 1951
END_YEAR = 1952

def days_list():
    # Define the start and end dates
    start_date = datetime(START_YEAR, 1, 1)
    end_date = datetime(END_YEAR, 12, 31)

    # Initialize the current date
    current_date = start_date
    time = 0
    days = []
    # Loop through all dates in start and end date
    while current_date <= end_date:
        time = current_date.strftime('%d-%m-%Y')
        link = f"doctypes: kolkata fromdate: {time} todate: {time}"
        days.append(link)
        with open ("each_day.txt", "a") as f:
            f.write(f'{link}\n')
        current_date += timedelta(days=1)

    return days

if __name__ == "__main__":
    days_list()