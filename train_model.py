# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

# File paths
IN_FILE = "data/train_FD001.txt"
MODEL_FILE = "model.pkl"
SCALER_FILE = "scaler.pkl"
FEATURES_FILE = "features.pkl"

# ✅ 3 op_settings + 21 sensors = 24 features
FEATURES = ["op_setting1", "op_setting2", "op_setting3"] + [f"sensor{i}" for i in range(1, 22)]

def load_training_data(file_path):
    print("Loading training data...")
    # NASA CMAPSS FD001 = 26 cols
    col_names = ["unit", "cycle", "op_setting1", "op_setting2", "op_setting3"] + [f"sensor{i}" for i in range(1, 22)]
    df = pd.read_csv(file_path, sep="\s+", header=None)
    df.columns = col_names
    return df

def main():
    df = load_training_data(IN_FILE)

    # Compute RUL (Remaining Useful Life)
    df["RUL"] = df.groupby("unit")["cycle"].transform(max) - df["cycle"]

    # ✅ Select only the right columns instead of renaming
    X = df[FEATURES]
    y = df["RUL"]

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train model
    print("Training RandomForestRegressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)

    # Save model, scaler, and features
    joblib.dump(model, MODEL_FILE)
    joblib.dump(scaler, SCALER_FILE)
    joblib.dump(FEATURES, FEATURES_FILE)

    print(f"✅ Training complete. Saved {MODEL_FILE}, {SCALER_FILE}, {FEATURES_FILE}")

if __name__ == "__main__":
    main()
