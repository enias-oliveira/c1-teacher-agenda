from csv import DictReader

FILENAME = "appointments.csv"


def get_all_appointments():
    def convert_id_and_class_to_int(appointment):
        appointment["id"] = int(appointment["id"])
        appointment["class-number"] = int(appointment["class-number"])
        return appointment

        try:
            with open(FILENAME, "r") as readable:
                reader = DictReader(readable)
                return [
                    convert_id_and_class_to_int(appointment) for appointment in reader
                ]

        except FileNotFoundError:
            return []
