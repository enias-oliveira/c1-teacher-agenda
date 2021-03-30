from datetime import datetime

csv_date_to_datetime = lambda given_date: datetime.strptime(
    given_date, "%Y-%m-%d %H:%M:%S"
)
