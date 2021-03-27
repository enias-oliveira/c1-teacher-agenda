from flask import Flask, request


def create_app():
    app = Flask(__name__)

    @app.route("/appointment", methods=["POST"])
    def make_appointment():
        appointment = request.get_json()

        from services.save_to_csv import create_appointment

        service_response = create_appointment(appointment)

        if not service_response:
            return {}

        return service_response

    return app
