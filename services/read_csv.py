from csv import DictReader

from . import csv_date_to_datetime

FILENAME = "appointments.csv"


def get_all_appointments():
    def convert_id_and_class_to_int(appointment):
        appointment["id"] = int(appointment["id"])
        appointment["class-number"] = int(appointment["class-number"])
        return appointment

    with open(FILENAME, "r") as readable:
        reader = DictReader(readable)
        return [convert_id_and_class_to_int(appointment) for appointment in reader]


def get_appointment(target_id: int):
    appointments = get_all_appointments()
    return next(
        filter(lambda appointment: appointment["id"] == target_id, appointments), None
    )


def get_available_times(given_date) -> list:
    booked_times = get_all_booked_times_from_date(given_date)

    from datetime import time

    available_times = []

    i = 8
    while i < 23:
        time_i = time(i, 0, 0)

        if time_i not in booked_times:
            j = i + 1

            while j < 24:
                time_j = time(j, 0, 0)

                if time_j in booked_times or j == 23:
                    available_time = (
                        time_i,
                        time_j,
                    )
                    available_times.append(available_time)
                    i = j
                    break

                j += 1

        else:
            i += 1

    return available_times


def get_all_booked_times_from_date(given_date) -> list:
    appointments = get_all_appointments()
    appointments_dates = [
        csv_date_to_datetime(appointment["date"]) for appointment in appointments
    ]

    booked_times = [
        app_dt.time()
        for app_dt in appointments_dates
        if app_dt.date() == given_date.date()
    ]

    return booked_times
