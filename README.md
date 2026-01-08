# 🔐 Face Recognition Based Secure Access Control System
📌 Overview

This project implements a real-time Face Recognition Based Secure Access Control System using computer vision and machine learning techniques. The system authenticates individuals through live webcam input, grants or denies access based on facial similarity, and logs every access attempt into a MySQL database. A modern Streamlit web dashboard provides live monitoring, analytics, and log visualization.

🎯 Objectives

  To design a secure access control mechanism using facial biometrics

  To perform real-time face detection and recognition

  To log access attempts with confidence scores and timestamps

  To provide a user-friendly web-based monitoring dashboard

🧠 System Features

  ✅ Live face detection using webcam

  ✅ Face recognition using 128-D facial encodings

  ✅ Access decision logic (GRANTED / DENIED)

  ✅ MySQL database logging

  ✅ Streamlit dashboard with:

      Metrics cards

      Access summary chart

      Real-time logs table

  ✅ Auto-refresh monitoring interface

🛠️ Technologies Used

  Programming Language: Python

  Computer Vision: OpenCV

  Face Recognition: face_recognition (dlib-based)

  Database: MySQL

  Frontend / UI: Streamlit

  Visualization: Altair

  Version Control: Git & GitHub

📂 Project Structure
FaceRecognitionAccess/
│
├── app.py                         # Streamlit dashboard + live camera
├── live_recognition.py            # Standalone live recognition
├── encode_faces.py                # Face encoding generator
├── face_detection.py              # Face detection module
├── camera_test.py                 # Webcam test
├── encodings.pkl                  # Stored face encodings
├── haarcascade_frontalface_default.xml
├── dataset/                       # Face image dataset
│   ├── person1/
│   ├── person2/
│   └── ...
├── requirements.txt               # Python dependencies
├── .gitignore
└── venv/                          # Virtual environment

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/FaceRecognitionAccess.git
cd FaceRecognitionAccess

2️⃣ Create & Activate Virtual Environment
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash)

3️⃣ Install Dependencies
pip install -r requirements.txt

🗄️ Database Setup (MySQL)

Create database and table:

CREATE DATABASE face_access_db;

USE face_access_db;

CREATE TABLE access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_name VARCHAR(100),
    access_status VARCHAR(20),
    confidence FLOAT,
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

📸 Dataset Preparation

Create folders inside dataset/ with person names

Capture 10–20 images per person

Include different angles and lighting conditions

Re-run encoding script after changes

python encode_faces.py

▶️ Running the Application
Start Streamlit Dashboard
streamlit run app.py


Then open in browser:

http://localhost:8501

📊 Dashboard Capabilities

Live webcam recognition

Access Granted / Denied metrics

Bar chart (Granted vs Denied)

Real-time MySQL access logs

🔐 Access Control Logic
Condition	Action
Face matched + confidence ≥ threshold	ACCESS GRANTED
Face not matched / low confidence	ACCESS DENIED
🧪 Testing & Observations

Tested under different lighting conditions

Accuracy depends on dataset quality

Performance optimized by frame resizing

⚠️ Limitations

  Accuracy drops in low-light environments
  
  Sensitive to camera quality
  
  Single-camera support only

🚀 Future Enhancements

  Multi-camera support
  
  Liveness detection (anti-spoofing)
  
  Mobile app integration
  
  Cloud database deployment

  Role-based access levels

👩‍💻 Author
Sridevi Lavanya M anf Dinesh S
M.Tech - AI & DS

📜 License
This project is for academic and educational purposes.
