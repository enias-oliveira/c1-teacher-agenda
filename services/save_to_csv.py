from datetime import datetime, time

from .read_csv import get_all_appointments


def get_new_id():
    appointments = get_all_appointments()

    if not appointments:
        return 1

    id_list = [appointment["id"] for appointment in appointments]
    last_id = id_list[-1]

    return last_id + 1


def is_service_time(given_time):
    open_time = time(8, 0, 0)
    close_time = time(23, 0, 0)

    return given_time >= open_time and given_time <= close_time


def csv_date_to_datetime(given_date: str):
    return datetime.strptime(given_date, "%Y-%m-%d %H:%M:%S")


def is_date_available(given_date: str):
    given_datetime = csv_date_to_datetime(given_date)
    given_time = given_datetime.time()

    if not is_service_time(given_time):
        return False

    appointments = get_all_appointments()

    appointments_dates_in_given_datetime = [
        csv_date_to_datetime(app_dt["date"])
        for app_dt in appointments
        if csv_date_to_datetime(app_dt["date"]) == given_datetime
    ]

    if appointments_dates_in_given_datetime:
        return False

    return True


def create_appointment(new_appointment: dict):

    if not is_date_available(new_appointment["date"]):
        return {}

    new_id = get_new_id()

    return {"id": new_id}
