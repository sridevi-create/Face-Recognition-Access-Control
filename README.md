# 🔐 Face Recognition Based Secure Access Control System
📌 Overview

This project implements a real-time Face Recognition Based Secure Access Control System using computer vision and machine learning techniques. The system authenticates individuals through live webcam input, grants or denies access based on facial similarity, and logs every access attempt into a MySQL database. A modern Streamlit web dashboard provides live monitoring, analytics, and log visualization.

# 🎯 Objectives

  To design a secure access control mechanism using facial biometrics

  To perform real-time face detection and recognition

  To log access attempts with confidence scores and timestamps

  To provide a user-friendly web-based monitoring dashboard

# 🧠 System Features

  ✅ Live face detection using webcam

  ✅ Face recognition using 128-D facial encodings

  ✅ Access decision logic (GRANTED / DENIED)

  ✅ MySQL database logging

  ✅ Streamlit dashboard with:

      Metrics cards

      Access summary chart

      Real-time logs table

  ✅ Auto-refresh monitoring interface

# 🛠️ Technologies Used

  Programming Language: Python

  Computer Vision: OpenCV

  Face Recognition: face_recognition (dlib-based)

  Database: MySQL

  Frontend / UI: Streamlit

  Visualization: Altair

  Version Control: Git & GitHub

# 📂 Project Structure
FaceRecognitionAccess/
│
├── app.py
├── encode_faces.py
├── live_recognition.py
├── face_detection.py
├── haarcascade_frontalface_default.xml
├── requirements.txt
├── .gitignore
│
├── dataset/                 # (Ignored – contains face images)
├── encodings.pkl            # (Ignored – generated file)
├── venv/                    # (Ignored – virtual environment)



# 📊 Dashboard Overview

  Total Attempts – Total number of access requests  
  Access Granted – Successful recognitions
  Access Denied – Unauthorized attempts
  Bar Chart Visualization – Real-time access decision summary
  Live Camera Feed – Face detection and recognition overlay

# 🔐 Access Decision Logic

  Face is detected from the live camera feed
  Face encoding is compared with stored encodings
  If distance < threshold → Access Granted
  Else → Access Denied
  Each attempt is logged with timestamp and status

# ⚠️ Privacy & Security Notice

  The dataset/ folder containing face images is intentionally excluded from the repository
  The encodings.pkl file is also excluded as it is generated locally
  Users must create their own dataset and regenerate encodings

# 📦 How to Run Locally :

    git clone https://github.com/<your-username>/FaceRecognitionAccess.git
    cd FaceRecognitionAccess
    pip install -r requirements.txt
    python encode_faces.py
    streamlit run app.py

# 🧠 Academic Significance
This project demonstrates:

  Practical application of biometric security systems
  Integration of AI with web-based dashboards
  Real-time decision-making using computer vision
  Secure database-driven logging and monitoring

# 👩‍💻 Author
Sridevi Lavanya M and Dinesh S
M.Tech - AI & DS

# 📜 License
This project is for academic and educational purposes.
