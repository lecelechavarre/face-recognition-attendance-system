***Real-Time Student Attendance System (Python)***

A real-time student attendance system built with Python that uses Facenet for facial recognition, SVM for face classification, and Haar cascades for anti-spoofing — ensuring accurate and secure attendance tracking.
This system also includes hand-raising detection for monitoring student participation and a face login feature for user authentication.

Features

Real-Time Facial Recognition using Facenet

Anti-Spoofing System via Haar cascades

Hand-Raising Detection for class participation

Face-Based Login authentication

Automated Attendance Recording stored securely in a database

***Tech Stack***

Languages: Python
Libraries & Frameworks: Facenet, OpenCV, TensorFlow, Scikit-learn (SVM), Haar Cascades
Database: MySQL
Tools: Conda, PyCharm, Pandas, APScheduler, gTTS

⚙️ Installation Guide
1. Install Conda

  1.1 If you don’t have Conda installed, download and install either
Miniconda
 or Anaconda
.

2. Create a New Environment
  2.1 conda create -n attendance python=3.6
  2.2 conda activate attendance

3. Install Dependencies
```
pip install --upgrade pip
pip install opencv-python==4.2.0.34
pip install tensorflow==2.4.0
pip install sklearn==0.0
pip install Pillow
pip install PyMySQL
pip install pandas
pip install gTTS
pip install APScheduler
```

4. Set Up the Database

   4.1 Open your database management tool (e.g., phpMyAdmin or MySQL Workbench).

   4.2 Create a new database named recognition.

   4.3 Import the provided recognition.sql file from the project folder.

▶ Running the Project
```bash
python main.py
```


After launching, the system will initialize your webcam for facial recognition and start processing real-time attendance.

***Key Functionalities***

Feature	Description
Facial Recognition	Identifies and verifies students in real time using Facenet.
Anti-Spoofing	Detects fake inputs (photos or videos) using Haar cascades.
Hand Raise Detection	Recognizes student participation gestures.
Face Login	Allows users to log in securely through facial verification.
```
🧩 Folder Structure
├── dataset/             # Stores captured student images
├── models/              # Pre-trained Facenet and SVM models
├── recognition.sql      # Database schema
├── main.py              # Main program file
├── utils/               # Helper functions and modules
└── README.md
```
