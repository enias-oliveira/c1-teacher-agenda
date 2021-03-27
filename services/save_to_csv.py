from .read_csv import get_all_appointments


def get_new_id():
    appointments = get_all_appointments()

    if not appointments:
        return 1

    id_list = [appointment["id"] for appointment in appointments]
    last_id = id_list[-1]

    return last_id + 1


def create_appointment(new_appointment: dict):
    new_id = get_new_id()

    return {"id": new_id}
