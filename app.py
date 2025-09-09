# app.py
from flask import Flask, render_template, jsonify, request, send_file
import model as ml

# --------------------------
# Initialize Flask app
# --------------------------
app = Flask(
    __name__,
    template_folder="templates",  # HTML templates
    static_folder="static"        # not used much since HTML is self-contained
)

# --------------------------
# Frontend Route
# --------------------------
@app.route("/")
def index():
    return render_template("index.html")

# --------------------------
# API: Machines Data
# --------------------------
@app.route("/api/machines")
def api_machines():
    try:
        data = ml.simulate_sensor_trends()  # upgraded advanced AI model
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------------
# API: PDF Report
# --------------------------
@app.route("/api/report_pdf")
def api_report_pdf():
    machine = request.args.get("machine", "Machine_1")
    try:
        pdf_path = ml.generate_pdf_report(machine)
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------------
# Run the Flask App
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)
