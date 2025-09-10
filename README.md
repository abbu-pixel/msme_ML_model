⚙️ Smart IoT Machine Monitoring Dashboard

Real-time simulation and monitoring of industrial machines using Python, Streamlit, and Machine Learning. This project demonstrates predictive maintenance, sensor trends, and risk analysis for multiple machines.

🚀 Features

Real-time Machine Monitoring

Auto-updating dashboard every 5 seconds

Displays machine health, RUL (Remaining Useful Life), risk scores, and operational status

Advanced Sensor Simulation

Temperature, vibration, pressure, humidity, current, voltage, noise, torque, oil quality

Realistic trends with noise and anomalies

Multiple failure modes: thermal, mechanical, hydraulic, electrical, mixed

Predictive Insights

Risk assessment and confidence scores

Sensor history visualization (last 40 time-steps)

Interactive Dashboard

Streamlit-based UI with graphs, tables, and metrics

Download PDF reports per machine

Multi-Machine Support

Monitor multiple machines simultaneously

Easy scalability for industrial-scale applications

📊 Dashboard Screenshot


Displays machine metrics, risk, sensor history, and download option.

🛠️ Tech Stack

Frontend & Visualization: Streamlit, Plotly, Matplotlib

Backend & Simulation: Python, NumPy, Pandas

PDF Reporting: ReportLab

⚙️ Installation
# Clone repository
git clone https://github.com/abbu-pixel/msme_ML_model.git
cd msme_ML_model

# Install dependencies
pip install -r requirements.txt

🏃 Running the Dashboard
streamlit run app.py


The dashboard will open in your default browser

Auto-refresh is enabled for real-time simulation

Use download buttons to save machine reports as PDFs

📁 Project Structure
msme_ML_model/
│
├─ app.py                 # Main Streamlit application
├─ model.py               # Machine simulation and ML logic
├─ requirements.txt       # Python dependencies
├─ templates/             # Optional HTML templates
├─ static/                # Optional static files (CSS, images)
├─ README.md              # Project documentation
└─ reports/               # Generated PDF reports

🔧 Future Improvements

Integrate real IoT sensors for live data

Add ML predictive models for failure forecasting

Multi-user dashboard with authentication & role management

Real-time notifications on critical events

📌 References

Streamlit Documentation

ReportLab Documentation

Plotly Documentation

📄 License

This project is licensed under the MIT License.
