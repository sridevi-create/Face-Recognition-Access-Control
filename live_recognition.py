import mysql.connector
import cv2
import face_recognition
import pickle

# ---------- MySQL connection ----------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="$Sri29$",
    database="face_access_db"
)
cursor = db.cursor()

# ---------- Load encodings ----------
with open("encodings.pkl", "rb") as f:
    known_encodings, known_names = pickle.load(f)

print("Encodings loaded. Starting camera...")

# ---------- Open camera ----------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not accessible")
    exit()

# ---------- Main loop ----------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(
        rgb_frame, face_locations
    )

    for (top, right, bottom, left), face_encoding in zip(
        face_locations, face_encodings
    ):

        face_distances = face_recognition.face_distance(
            known_encodings, face_encoding
        )
        best_match_index = face_distances.argmin()

        confidence = 1 - face_distances[best_match_index]

        if face_distances[best_match_index] < 0.45:
            name = known_names[best_match_index]
            access = "GRANTED"
        else:
            name = "Unknown"
            access = "DENIED"

        # ---------- Log to MySQL ----------
        sql = """
        INSERT INTO access_logs (person_name, access_status, confidence)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (name, access, confidence))
        db.commit()

        # ---------- Draw on frame ----------
        cv2.rectangle(
            frame, (left, top), (right, bottom), (0, 255, 0), 2
        )
        cv2.putText(
            frame,
            name,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2
        )

    cv2.imshow("DAY 6 - Access Control System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
