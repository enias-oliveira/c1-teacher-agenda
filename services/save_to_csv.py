from csv import DictWriter
from datetime import datetime, time

from .read_csv import get_all_appointments, get_appointment


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


csv_date_to_datetime = lambda given_date: datetime.strptime(
    given_date, "%Y-%m-%d %H:%M:%S"
)


def hour_rounder(given_date_obj):
    return given_date_obj.replace(
        second=0, microsecond=0, minute=0, hour=given_date_obj.hour
    )


def is_date_available(given_datetime: datetime):
    rounded_hour_date = hour_rounder(given_datetime)
    rounded_hour_time = rounded_hour_date.time()

    if not is_service_time(rounded_hour_time):
        return False

    appointments = get_all_appointments()

    appointments_already_booked = [
        "Booked"
        for appointment in appointments
        if appointment["date"] == rounded_hour_date.__str__()
    ]

    if appointments_already_booked:
        return False

    return True


def write_new_appointment(new_appointment: dict):
    FIELDNAMES = [
        "id",
        "date",
        "name",
        "school-subjects",
        "difficulty",
        "class-number",
        "_growth",
    ]

    with open("appointments.csv", "a+") as writable_file:
        writer = DictWriter(writable_file, fieldnames=FIELDNAMES)
        writer.writerow(new_appointment)


def create_appointment(new_appointment: dict):
    new_appointment_datetime = csv_date_to_datetime(new_appointment["date"])

    if not is_date_available(new_appointment_datetime):
        return {}

    new_id = get_new_id()
    rounded_date = hour_rounder(new_appointment_datetime)

    del new_appointment["date"]

    processed_new_appointment = {
        "id": new_id,
        "date": rounded_date.__str__(),
        **new_appointment,
    }

    write_new_appointment(processed_new_appointment)

    return get_appointment(new_id)
