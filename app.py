from flask import Flask

from routes.api.vending_machine_routes import vending_machine_controller

app = Flask(__name__)
app.register_blueprint(vending_machine_controller)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
