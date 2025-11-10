from apscheduler.schedulers.background import BackgroundScheduler
import pymysql
from datetime import datetime
import smtplib
from mark_attendance import Mark_Attendance
from email.message import EmailMessage
import os  # Add this line to import the 'os' module
import pandas as pd  # Add this line to import the 'pandas' module
from tkinter import messagebox
def all_students():
    conn = pymysql.connect(host="localhost", user="root", password="", database="recognition")
    cur = conn.cursor()
    cur.execute("SELECT eid, email_address, guardian_email FROM attendance")
    data = cur.fetchall()
    students = {id: (email, guardian_email) for id, email, guardian_email in data}
    conn.close()
    return students

def get_registered_student_ids(date):
    conn = pymysql.connect(host="localhost", user="root", password="", database="recognition")
    cur = conn.cursor()
    cur.execute("SELECT id FROM report WHERE date = %s", (date,))
    registered_student_ids = [row[0] for row in cur.fetchall()]
    conn.close()
    return registered_student_ids

def get_absent_student_ids(students, registered_student_ids):
    all_student_ids = students.keys()
    absent_student_ids = [id for id in all_student_ids if id not in registered_student_ids]
    return absent_student_ids
def get_student_email(student_id):
    # Placeholder function, replace with your actual implementation to retrieve email address
    # Assuming you have a database query to fetch email addresses based on student IDs
    conn = pymysql.connect(host="localhost", user="root", password="", database="recognition")
    cur = conn.cursor()
    cur.execute("SELECT email_address FROM attendance WHERE eid = %s", (student_id,))
    email_address = cur.fetchone()[0]
    conn.close()
    return email_address
def get_admin_email(department):
    # Manually specify the teacher's email address
    admin_email = "ricapintoy@gmail.com"
    return admin_email


def send_mail():
    dt = datetime.now()
    date = dt.strftime("%Y-%m-%d")

    # Fetch attendance data for the given date
    conn = pymysql.connect(host="localhost", user="root", password="", database="recognition")
    cur = conn.cursor()
    cur.execute("SELECT id, name, date, time, status FROM report WHERE date = %s", (date,))
    attendance_data = cur.fetchall()
    conn.close()

    # Send email to students
    for row in attendance_data:
        id, name, attendance_date, time, status = row
        email_content = f"Dear {name},\n\n"
        email_content += f"This email confirms that you attended on {attendance_date}. You were marked as {status} at {time}.\n\n"
        email_content += "Thank you for your attention to attendance.\n\n"

        # Retrieve student email using the get_student_email function
        student_email = get_student_email(id)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('ricapintoy@gmail.com', 'hppzxjemjiqklxng')  # Replace with your email credentials
            server.sendmail('ricapintoy@gmail.com', student_email, email_content)

    if attendance_data:
        print("Emails sent successfully")
    else:
        print("No attendance data found for the date. No emails sent.")

    # Send the attendance file to the teacher's email
    

