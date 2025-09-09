# model.py
import numpy as np
import random
import os

MACHINE_COUNT = 5
TIME_STEPS = 20  # Number of points in trend graphs

def simulate_sensor_trends(n_machines=MACHINE_COUNT):
    """
    Generate realistic machine data with trends:
    - 3 OK machines
    - 1 Warning
    - 1 Critical
    """
    results = {}
    predefined_status = ["OK", "OK", "OK", "Warning", "Critical"]

    for i in range(1, n_machines + 1):
        machine_name = f"Machine_{i}"
        status_type = predefined_status[i-1]

        # Base values per status
        if status_type == "OK":
            base_health = 90
            base_rul = 220
            fluctuation = 0.5
        elif status_type == "Warning":
            base_health = 65
            base_rul = 150
            fluctuation = 1.0
        else:  # Critical
            base_health = 30
            base_rul = 60
            fluctuation = 2.0

        # Generate realistic trends
        health_trend = [base_health]
        rul_trend = [base_rul]
        temperature_trend = [70 + i*2]
        vibration_trend = [0.2 + i*0.05]
        pressure_trend = [5 + i*0.2]

        for t in range(1, TIME_STEPS):
            health_trend.append(np.clip(health_trend[-1] + np.random.normal(0, fluctuation), 10, 100))
            rul_trend.append(np.clip(rul_trend[-1] + np.random.normal(0, fluctuation*5), 0, 250))
            temperature_trend.append(np.clip(temperature_trend[-1] + np.random.normal(0, fluctuation), 60, 100))
            vibration_trend.append(np.clip(vibration_trend[-1] + np.random.normal(0, fluctuation*0.05), 0.1, 1.0))
            pressure_trend.append(np.clip(pressure_trend[-1] + np.random.normal(0, fluctuation*0.2), 3, 10))

        # Current values = last point
        health = round(health_trend[-1], 1)
        rul = round(rul_trend[-1], 2)
        temperature = round(temperature_trend[-1], 1)
        vibration = round(vibration_trend[-1], 2)
        pressure = round(pressure_trend[-1], 1)
        working_hours = random.randint(500, 5000)

        # Only Critical machine shows anomaly
        anomaly = True if status_type == "Critical" else False

        # Confidence
        confidence = round(random.uniform(0.8, 0.99), 2)

        results[machine_name] = {
            "status": status_type,
            "health": health,
            "rul": rul,
            "temperature": temperature,
            "vibration": vibration,
            "pressure": pressure,
            "working_hours": working_hours,
            "anomaly": anomaly,
            "confidence": confidence,
            "history": {
                "health": health_trend,
                "rul": rul_trend,
                "temperature": temperature_trend,
                "vibration": vibration_trend,
                "pressure": pressure_trend
            }
        }

    return results

def generate_pdf_report(machine_name):
    """Dummy PDF report generation"""
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    pdf_path = os.path.join(report_dir, f"{machine_name}_report.pdf")
    
    if not os.path.exists(pdf_path):
        with open(pdf_path, "wb") as f:
            f.write(b"%PDF-1.4\n%Dummy PDF content\n")
    return pdf_path
