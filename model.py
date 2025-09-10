import numpy as np
import random
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest

TIME_STEPS = 40
machine_states = {}

def init_machine(machine_name, status_type, mode):
    if status_type == "OK":
        health, rul = 100, 250
    elif status_type == "Warning":
        health, rul = 70, 150
    else:
        health, rul = 40, 80

    return {
        "status": status_type,
        "mode": mode,
        "health_trend": [health],
        "rul_trend": [rul],
        "temperature_trend": [70 + random.uniform(-2,2)],
        "vibration_trend": [0.2 + random.uniform(-0.05,0.05)],
    }

def simulate_sensor_trends():
    global machine_states
    predefined_status = ["OK","Warning","Critical"]
    failure_modes = ["thermal","mechanical","hydraulic"]

    if not machine_states:
        for i, status in enumerate(predefined_status, 1):
            mode = failure_modes[i-1]
            machine_states[f"Machine_{i}"] = init_machine(f"Machine_{i}", status, mode)

    results = {}
    for name, state in machine_states.items():
        # Degrade health
        new_health = max(5, state["health_trend"][-1] - random.uniform(0.05, 0.3))
        state["health_trend"].append(new_health)

        # RUL countdown
        new_rul = max(0, state["rul_trend"][-1] - random.uniform(0.5, 1.0))
        state["rul_trend"].append(new_rul)

        # Sensor updates
        new_temp = 70 + (100-new_health)*0.25 + random.uniform(-0.5,0.5)
        new_vib = 0.2 + (100-new_health)*0.01 + random.uniform(-0.01,0.01)
        state["temperature_trend"].append(new_temp)
        state["vibration_trend"].append(new_vib)

        # Predict RUL using last 10 steps
        X = np.arange(len(state["rul_trend"][-10:])).reshape(-1,1)
        y = np.array(state["rul_trend"][-10:])
        model = LinearRegression()
        model.fit(X, y)
        predicted_rul = max(0, model.predict(np.array([[10]]))[0])

        # Anomaly detection
        iso = IsolationForest(contamination=0.1)
        data = np.array(state["temperature_trend"][-10:]+state["vibration_trend"][-10:]).reshape(-1,2)
        try:
            anomaly = iso.fit_predict(data.reshape(-1,2))[-1] == -1
        except:
            anomaly = False

        results[name] = {
            "status": state["status"],
            "mode": state["mode"],
            "health": round(new_health,1),
            "rul": round(new_rul,1),
            "predicted_rul": round(predicted_rul,1),
            "temperature": round(new_temp,1),
            "vibration": round(new_vib,2),
            "anomaly": anomaly,
            "history": {
                "health": state["health_trend"],
                "rul": state["rul_trend"],
                "temperature": state["temperature_trend"],
                "vibration": state["vibration_trend"]
            }
        }

    return results
