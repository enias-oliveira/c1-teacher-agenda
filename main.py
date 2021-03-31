from flask import Flask, request
from http import HTTPStatus
import json


def create_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    @app.route("/appointment")
    def list_appointment():
        from services.read_csv import get_all_appointments

        appointments = get_all_appointments()

        def drop_empty_growth(appointment):
            if not appointment["_growth"]:
                del appointment["_growth"]
            return appointment

        response = [drop_empty_growth(appointment) for appointment in appointments]

        return json.dumps(response), HTTPStatus.OK

    @app.route("/appointment", methods=["POST"])
    def make_appointment():
        appointment = request.get_json()

        from services.save_to_csv import create_appointment

        service_response = create_appointment(appointment)

        if not service_response:
            return {}, HTTPStatus.UNPROCESSABLE_ENTITY

        if not service_response["_growth"]:
            del service_response["_growth"]

        return service_response, HTTPStatus.OK

    @app.route("/appointment/available_times_on_the_day")
    def available_times():
        request_date = request.args.get("date")

        from datetime import datetime
        from services.read_csv import get_available_times

        request_date_dt = datetime.strptime(request_date, "%d%m%Y")
        available_times = get_available_times(request_date_dt)

        format_avlb_time = (
            lambda available_time: f"{available_time[0]:%H:%M}-{available_time[1]:%H:%M}"
        )

        formatted_available_times = [
            format_avlb_time(available_time) for available_time in available_times
        ]

        return {"available-times": formatted_available_times}

    @app.route("/appointment/<int:app_id>", methods=["PATCH"])
    def update_appointment(app_id):
        request_date = request.get_json()["date"]

        from services.save_to_csv import update_appointment_date

        request_response = update_appointment_date(app_id, request_date)

        if not request_response:
            return {}, HTTPStatus.UNPROCESSABLE_ENTITY

        return request_response, HTTPStatus.OK

    @app.route("/appointment/<int:app_id>", methods=["DELETE"])
    def delete_appointment(app_id):

        from services.save_to_csv import delete_appointment_from_csv

        request_response = delete_appointment_from_csv(app_id)

        if not request_response:
            return {"msg": "ID not found"}, HTTPStatus.UNPROCESSABLE_ENTITY

        return {}, HTTPStatus.NO_CONTENT

    return app
