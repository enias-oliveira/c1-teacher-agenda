from csv import DictReader

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
