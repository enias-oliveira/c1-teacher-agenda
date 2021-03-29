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

    return app
