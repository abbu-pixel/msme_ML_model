import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from io import BytesIO
from reportlab.pdfgen import canvas
import model  # your upgraded model.py

st.set_page_config(page_title="Smart IoT Dashboard", layout="wide")

st.title("⚙️ Smart IoT Machine Monitoring Dashboard")
st.markdown("Real-time machine health and sensor simulation (auto-updating every 5s)")

# -------------------------------
# Auto-refresh every 5 seconds
# -------------------------------
if "refresh_counter" not in st.session_state:
    st.session_state.refresh_counter = 0
st.session_state.refresh_counter += 1
st.experimental_rerun() if st.session_state.refresh_counter % 5 == 0 else None

# -------------------------------
# Simulate machine data
# -------------------------------
data = model.simulate_sensor_trends()
machines = list(data.keys())

# -------------------------------
# Helper: Create PDF
# -------------------------------
def create_pdf(machine_data, machine_name):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, f"{machine_name} - Machine Report")
    c.setFont("Helvetica", 12)
    y = 760
    for key in ["health", "rul", "temperature", "vibration", "pressure"]:
        c.drawString(50, y, f"{key.capitalize()}: {machine_data.get(key, 'N/A')}")
        y -= 20
    c.save()
    buffer.seek(0)
    return buffer

# -------------------------------
# Display multiple machines
# -------------------------------
for machine_name in machines:
    machine_data = data[machine_name]
    st.subheader(f"🏭 {machine_name}")

    # Info columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Health (%)", machine_data["health"])
    col2.metric("RUL (hrs)", machine_data["rul"])
    col3.metric("Confidence", f"{machine_data['confidence']*100:.1f}%")
    col4.metric("Status", machine_data["status"])

    # Interactive Graphs with Plotly
    sensors = ["health", "rul", "temperature", "vibration", "pressure"]
    fig = go.Figure()
    for sensor in sensors:
        history = machine_data["history"].get(sensor, [])
        fig.add_trace(go.Scatter(
            y=history,
            mode="lines+markers",
            name=sensor.capitalize()
        ))
    fig.update_layout(
        title=f"{machine_name} - Sensor Trends",
        xaxis_title="Time Steps",
        yaxis_title="Values",
        template="plotly_white",
        legend=dict(orientation="h", y=-0.3)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Anomaly
    if machine_data["anomaly"]:
        st.warning(f"⚠️ Anomaly detected in {machine_name}!")

    # Download PDF button
    pdf_buffer = create_pdf(machine_data, machine_name)
    st.download_button(
        label="⬇️ Download Report as PDF",
        data=pdf_buffer,
        file_name=f"{machine_name}_report.pdf",
        mime="application/pdf",
        key=f"download_{machine_name}_{st.session_state.refresh_counter}"
    )

st.markdown("---")
st.info("Dashboard auto-refreshes every 5 seconds. Interactive graphs powered by Plotly 🚀")
