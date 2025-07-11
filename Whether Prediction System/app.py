# app.py
from flask import Flask, render_template, request
from weather.routes import bp as weather_bp
from weather.model import predict as predict_weather

def create_app():
    # Tell Flask where to find templates and static assets
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.register_blueprint(weather_bp, url_prefix="/api")

    # Simple browser UI
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/result", methods=["POST"])
    def result():
        # Collect form data and cast numeric fields
        data = {k: v for k, v in request.form.items()}
        for field in ["precipitation", "temp_max", "temp_min", "wind"]:
            try:
                data[field] = float(data.get(field, 0))
            except ValueError:
                data[field] = 0.0

        prediction = predict_weather(data)
        return render_template("result.html", prediction=prediction)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)          # switch to False in prod