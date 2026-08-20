import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# --- 1. PREPARE THE DATA ---
# This acts as our historical network traffic database
data = {
    'packet_size_kb': [120, 45, 800, 30, 20, 1500, 50, 60, 900, 10],
    'failed_logins': [0, 0, 5, 1, 0, 12, 0, 0, 8, 0],
    'duration_seconds': [10, 5, 120, 15, 2, 300, 8, 12, 200, 1],
    'is_threat': [0, 0, 1, 0, 0, 1, 0, 0, 1, 0] # 1 means Threat, 0 means Safe
}
df = pd.DataFrame(data)

# --- 2. TRAIN THE MACHINE LEARNING MODEL ---
X = df[['packet_size_kb', 'failed_logins', 'duration_seconds']]
y = df['is_threat']

# We use a Random Forest algorithm to learn the patterns of a threat
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# --- 3. BUILD THE USER INTERFACE ---
st.set_page_config(page_title="Threat Detector", page_icon="🛡️")
st.title("🛡️ Cyber Threat Detection System")
st.write("Enter network connection details below to scan for potential anomalies.")

# Create 3 columns for a clean layout
col1, col2, col3 = st.columns(3)

with col1:
    packet_size = st.number_input("Packet Size (KB)", min_value=0, value=100)
with col2:
    failed_logins = st.number_input("Failed Logins", min_value=0, max_value=50, value=0)
with col3:
    duration = st.number_input("Duration (Seconds)", min_value=0, value=10)

st.markdown("---")

# --- 4. HANDLE THE ANALYSIS ---
if st.button("🔍 Analyze Connection", use_container_width=True):
    # Format the user's input so the model can read it
    input_data = [[packet_size, failed_logins, duration]]
    
    # Ask the ML model to predict if it's a threat
    prediction = model.predict(input_data)
    
    # Display the result to the user
    if prediction[0] == 1:
        st.error("🚨 THREAT DETECTED! Anomalous network behavior recognized.")
        st.warning("Action: Block IP Address and alert the administrator.")
    else:
        st.success("✅ Connection is safe. Normal traffic patterns observed.")