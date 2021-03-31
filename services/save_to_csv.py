from csv import DictWriter
from datetime import datetime, time

from . import csv_date_to_datetime
from .read_csv import (
    get_all_appointments,
    get_appointment,
    get_all_booked_times_from_date,
)


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


def hour_rounder(given_date_obj):
    return given_date_obj.replace(
        second=0, microsecond=0, minute=0, hour=given_date_obj.hour
    )


def is_date_available(given_datetime: datetime):
    rounded_hour_date = hour_rounder(given_datetime)
    rounded_hour_time = rounded_hour_date.time()

    if not is_service_time(rounded_hour_time):
        return False

    booked_appointments = get_all_booked_times_from_date(given_datetime)

    for booked_appointment in booked_appointments:
        if booked_appointment == rounded_hour_time:
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

    FILENAME = "appointments.csv"

    with open(FILENAME, "a") as writable_file:
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


def write_all_appointments(appointments: list):
    FIELDNAMES = [
        "id",
        "date",
        "name",
        "school-subjects",
        "difficulty",
        "class-number",
        "_growth",
    ]

    with open("appointments.csv", "w+") as writable_file:
        writer = DictWriter(writable_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(appointments)


def update_appointment_date(target_id: int, given_date: str) -> dict:
    target_appointment = get_appointment(target_id)
    target_appointment.update({"date": given_date})

    target_dt = csv_date_to_datetime(given_date)

    if not is_date_available(target_dt):
        return {}

    appointments = get_all_appointments()
    updated_appointments = [
        appointment if appointment["id"] != target_id else target_appointment
        for appointment in appointments
    ]

    write_all_appointments(updated_appointments)

    return get_appointment(target_id)
