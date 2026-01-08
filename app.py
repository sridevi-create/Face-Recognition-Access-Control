import streamlit as st
import mysql.connector
import pandas as pd
import time
import altair as alt
import cv2
import face_recognition
import pickle

# ---------- Page Config ----------
st.set_page_config(
    page_title="Face Recognition Access Control",
    layout="wide"
)

REFRESH_INTERVAL = 5  # seconds

# ---------- Session State (Rate Limiting) ----------
if "last_log_time" not in st.session_state:
    st.session_state.last_log_time = 0

# ---------- Load Encodings ----------
@st.cache_resource
def load_encodings():
    with open("encodings.pkl", "rb") as f:
        return pickle.load(f)

known_encodings, known_names = load_encodings()

# ---------- Custom CSS ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}
.metric-card {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
}
.metric-title { color: #ccc; font-size: 18px; }
.metric-value { font-size: 42px; font-weight: bold; }
.total { color: #4da6ff; }
.granted { color: #00ff99; }
.denied { color: #ff4b4b; }
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- Titles ----------
st.markdown("# 🔐 Face Recognition Based Secure Access Control System")
st.markdown("### Live Access Monitoring Dashboard")

# ---------- MySQL ----------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="$Sri29$",
    database="face_access_db"
)

query = "SELECT * FROM access_logs ORDER BY access_time DESC"
df = pd.read_sql(query, db)

# ---------- Metrics ----------
total_attempts = len(df)
granted_count = len(df[df["access_status"] == "GRANTED"])
denied_count = len(df[df["access_status"] == "DENIED"])

col1, col2, col3 = st.columns(3)
col1.markdown(f"<div class='metric-card'><div class='metric-title'>Total</div><div class='metric-value total'>{total_attempts}</div></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-card'><div class='metric-title'>Granted</div><div class='metric-value granted'>{granted_count}</div></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-card'><div class='metric-title'>Denied</div><div class='metric-value denied'>{denied_count}</div></div>", unsafe_allow_html=True)

st.divider()

# ---------- Chart ----------
chart_df = pd.DataFrame({
    "Access Type": ["Granted", "Denied"],
    "Count": [granted_count, denied_count]
})

chart = alt.Chart(chart_df).mark_bar().encode(
    x="Access Type",
    y="Count",
    color=alt.Color(
        "Access Type",
        scale=alt.Scale(domain=["Granted", "Denied"], range=["#00ff99", "#ff4b4b"]),
        legend=None
    )
)

st.altair_chart(chart, use_container_width=True)
st.divider()

# ---------- Live Camera ----------
st.subheader("🎥 Live Camera Access")
run_camera = st.checkbox("Start Camera")
FRAME_WINDOW = st.image([])

if run_camera:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("❌ Camera not accessible")
    else:
        while run_camera:
            ret, frame = cap.read()
            if not ret:
                break

            small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
            rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb)
            face_encodings = face_recognition.face_encodings(rgb, face_locations)

            # ---------- TASK 1: No Face ----------
            if len(face_locations) == 0:
                st.warning("⚠️ No face detected")
                FRAME_WINDOW.image(frame, channels="BGR")
                continue

            # ---------- TASK 2: Multiple Faces ----------
            if len(face_locations) > 1:
                st.error("❌ Multiple faces detected — access blocked")
                FRAME_WINDOW.image(frame, channels="BGR")
                continue

            # ---------- Recognition ----------
            for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
                distances = face_recognition.face_distance(known_encodings, encoding)
                best = distances.argmin()
                confidence = 1 - distances[best]

                # ---------- TASK 3: Confidence Levels ----------
                if distances[best] < 0.45:
                    name = known_names[best]
                    access = "GRANTED"
                    color = (0,255,0)
                elif distances[best] < 0.60:
                    name = "Uncertain"
                    access = "WARNING"
                    color = (0,255,255)
                    st.warning("⚠️ Low confidence match")
                else:
                    name = "Unknown"
                    access = "DENIED"
                    color = (0,0,255)

                # ---------- TASK 4: Rate Limit Logging ----------
                now = time.time()
                if now - st.session_state.last_log_time > 5:
                    cursor = db.cursor()
                    cursor.execute(
                        "INSERT INTO access_logs (person_name, access_status, confidence) VALUES (%s,%s,%s)",
                        (name, access, confidence)
                    )
                    db.commit()
                    st.session_state.last_log_time = now

                # Draw box
                top*=2; right*=2; bottom*=2; left*=2
                cv2.rectangle(frame, (left,top), (right,bottom), color, 2)
                cv2.putText(frame, f"{name} ({confidence:.2f})",
                            (left, top-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            FRAME_WINDOW.image(frame, channels="BGR")

        # ---------- TASK 5: Safe Release ----------
        cap.release()
        cv2.destroyAllWindows()

# ---------- Logs ----------
st.subheader("📄 Access Logs")
st.dataframe(df, use_container_width=True)

# ---------- Auto Refresh ----------
time.sleep(REFRESH_INTERVAL)
st.rerun()
