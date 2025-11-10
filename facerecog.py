
from tkinter import *
from datetime import datetime, timedelta
from tkinter import Tk, Button, Frame
from PIL import Image, ImageTk
import cv2
import os
from tkinter.ttk import Combobox, Treeview, Scrollbar, Progressbar
from PIL import Image, ImageTk
import pymysql
import csv
from LoginTraining import LoginTraining
from tkinter import messagebox, Message, ttk
import numpy as np
from os import listdir
from tkinter import Checkbutton, StringVar
from tkinter import simpledialog
import time
import random
import pandas as pd
from tkinter import filedialog
import gtts
from gtts import gTTS
from extract_embeddings import Extract_Embeddings
from LoginEmbeddingExtractor import LoginEmbeddingExtractor
import pickle
from training import Training
import os
from datetime import datetime
from statistics import mode
from mark_attendance import Mark_Attendance
import sys
import webbrowser
import re
import shutil
from apscheduler.schedulers.background import BackgroundScheduler
import event_scheduler
import json
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import model_from_json
import tensorflow as tf
import time
from datetime import datetime as dt, date
import cv2
from datetime import datetime
from event_scheduler import send_mail
from tkinter import OptionMenu, StringVar, Label
import os
import cv2
import pickle
import numpy as np
import winsound
import tkinter as tk
root_dir = os.getcwd()

try:
    embedding_obj = Extract_Embeddings(model_path = 'models/facenet_keras.h5')
    embedding_obj1 = LoginEmbeddingExtractor(model_path = 'models/facenet_keras.h5')

    embedding_model = embedding_obj.load_model()
    embedding_model1 = embedding_obj1.load_model()

    face_cascade = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml")

    # Load Model
    json_file = open('antispoofing_models/finalyearproject_antispoofing_model_mobilenet.json','r')
    loaded_model_json = json_file.read()
    json_file.close()
    liveness_model = model_from_json(loaded_model_json)
    # load weights into new model
    liveness_model.load_weights('antispoofing_models/finalyearproject_antispoofing_model_74-0.986316.h5')
    print("Liveness Model loaded successfully from disk")

except cv2.error as e:
    print("Error: Provide correct path for face detection model.")
    sys.exit(1)
except Exception as e:
    print("{}".format(str(e)))
    sys.exit(1)

    ############################################ Admin Login page #######################################################################


face = Tk()
face.title("Login Page")
face.geometry("1350x700+0+0")

        ##  variables for login  ##
username_var = StringVar()
password_var = StringVar()
user_type_var = StringVar()


def login(username=None):
 if username is None:
        username = username_var.get()  # Capture the username
        print("Username captured:", username)
        if username_var.get() == "" or password_var.get() == "":
            messagebox.showerror('Error','All the fields are required', parent = face)
        else:
            try:
                conn = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'recognition')
                curr = conn.cursor()
                curr.execute('SELECT * FROM login WHERE username = %s', (username,))
                row = curr.fetchone()
                if row == None:
                    messagebox.showerror('Error','Invalid Data')

                else:
                    global logged_in_username  # declare global variable
                    logged_in_username = username  # set the logged_in_username
                    face.destroy()
                    user_type_var.set("")
                    
                    # face_recognition_login(logged_in_username)
               

                    def manage_student():
                        try:
                            attendance1.destroy()
                            conn = pymysql.connect(host="localhost", user="root", password="", database="recognition")
                            cur = conn.cursor()
                            first = Toplevel()
                            first.geometry("1350x650")
                            first.config(bg="#FF9900")
                            first.title("Add Student")

                            # Create a frame
                            frame = Frame(first, bg="#FF9900")
                            frame.place(x=0, y=0, width=1350)
                            
                            def on_closing ():
                                 first.destroy()
                                 # Show the main window again
                                 open_admin_panel()
                            
                            first.protocol("WM_DELETE_WINDOW", on_closing)
                            # Place the label inside the frame
                            def back():
                                first.destroy()

                            # All Required variables for database
                            eid_var = StringVar()
                            post_var = StringVar()
                            fname_var = StringVar()
                            gender_var = StringVar()
                            contact_var = StringVar()
                            address_var = StringVar()
                            guardian_name_var = StringVar()
                            guardian_email_var = StringVar()
                            guardian_contact_var = StringVar()
                            dt = datetime.now()
                            DOJ_var = str(dt).split(' ')[0]
                            search_by = StringVar()
                            search_text = StringVar()
                            search_from = StringVar()
                            search_result = StringVar()
                            mydata = []
                            dataset_dir = os.path.join(root_dir, 'dataset')

                            ############################################# Functions of student Management form ##########################################

                            ########################################## To Add the student #####################################
                            def add_student ():
                                 conn = pymysql.connect(host="localhost", user="root", password="",
                                                        database="recognition")
                                 
                                 if post_var.get() == "" or fname_var.get() == "" or gender_var.get() == "" or contact_var.get() == "" or address_var.get() == "":
                                      messagebox.showerror("Error", "All fields are Required", parent=first)
                                 else:
                                      if (re.search('[a-zA-Z]+', fname_var.get())):
                                           if len(contact_var.get()) != 10:
                                                messagebox.showerror('Error', 'Contact Number must be 10 digits',
                                                                     parent=first)
                                           else:
                                                if (re.search('^[9]\d{9}$', contact_var.get())):
                                                     if re.search('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                                                                  address_var.get()):
                                                          cur_check = conn.cursor()
                                                          cur_check.execute(
                                                               "SELECT * FROM attendance WHERE email_address = %s",
                                                               (address_var.get(),))
                                                          existing_user = cur_check.fetchone()
                                                          if existing_user:
                                                               messagebox.showerror("Error",
                                                                                    "Email address already in use",
                                                                                    parent=first)
                                                          else:
                                                               regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
                                                               if (re.search(regex, address_var.get())):
                                                                    name = fname_var.get()
                                                                    input_directory = os.path.join(dataset_dir, name)
                                                                    if not os.path.exists(input_directory):
                                                                         os.makedirs(input_directory, exist_ok='True')
                                                                         count = 1
                                                                         print("[INFO] starting video stream...")
                                                                         video_capture = cv2.VideoCapture(1)
                                                                         while count <= 100:
                                                                              try:
                                                                                   check, frame = video_capture.read()
                                                                                   gray = cv2.cvtColor(frame,
                                                                                                       cv2.COLOR_BGR2GRAY)
                                                                                   faces = face_cascade.detectMultiScale(
                                                                                        gray, 1.3, 5)
                                                                                   for (x, y, w, h) in faces:
                                                                                        face = frame[y - 5:y + h + 5,
                                                                                               x - 5:x + w + 5]
                                                                                        resized_face = cv2.resize(face,
                                                                                                                  (160,
                                                                                                                   160))
                                                                                        cv2.imwrite(os.path.join(
                                                                                             input_directory,
                                                                                             name + str(
                                                                                                  count) + '.jpg'),
                                                                                                    resized_face)
                                                                                        cv2.rectangle(frame, (x, y),
                                                                                                      (x + w, y + h),
                                                                                                      (0, 0, 255), 2)
                                                                                        count += 1
                                                                                   
                                                                                   # show the output frame
                                                                                   cv2.imshow("Frame", frame)
                                                                                   key = cv2.waitKey(1)
                                                                                   if key == ord('q'):
                                                                                        break
                                                                              except Exception as e:
                                                                                   pass
                                                                         video_capture.release()
                                                                         cv2.destroyAllWindows()
                                                                         cur1 = conn.cursor()
                                                                         cur1.execute(
                                                                              "insert into attendance(department,fname,gender,contact_no,email_address,date_of_join,guardian_name,guardian_email,guardian_contact) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                                                              (
                                                                                   post_var.get(),
                                                                                   fname_var.get(),
                                                                                   gender_var.get(),
                                                                                   contact_var.get(),
                                                                                   address_var.get(),
                                                                                   DOJ_var,
                                                                                   guardian_name_var.get(),
                                                                                   guardian_email_var.get(),
                                                                                   guardian_contact_var.get()
                                                                              ))
                                                                         
                                                                         conn.commit()
                                                                         cur2 = conn.cursor()
                                                                         cur2.execute(
                                                                              "select eid from attendance where fname=%s ",
                                                                              (name,))
                                                                         output = cur2.fetchone()
                                                                         (id,) = output
                                                                         os.rename(os.path.join(dataset_dir, name),
                                                                                   os.path.join(dataset_dir,
                                                                                                name + "_" + str(id)))
                                                                         display()
                                                                         clear()
                                                                         conn.close()
                                                                         messagebox.showinfo("Success",
                                                                                             "All photos are collected",
                                                                                             parent=first)
                                                                    else:
                                                                         if len(os.listdir(input_directory)) == 100:
                                                                               messagebox.showwarning("Error",
                                                                                                     "Photo already added for this user.. Click Update to update photo",
                                                                                                     parent=first)
                                                                         else:
                                                                              ques = messagebox.askyesnocancel(
                                                                                   "Notification",
                                                                                   "Directory already exists with incomplete samples. Do you want to delete the directory",
                                                                                   parent=first)
                                                                              if (ques == True):
                                                                                   shutil.rmtree(input_directory)
                                                                                   messagebox.showinfo("Success",
                                                                                                       "Directory Deleted..Now you can add the photo samples",
                                                                                                       parent=first)
                                                               else:
                                                                    messagebox.showerror('Error',
                                                                                         'Please Enter the Valid Email Address',
                                                                                         parent=first)
                                                     else:
                                                          messagebox.showerror('Error',
                                                                               'Please Enter the Valid Email Address',
                                                                               parent=first)
                                                else:
                                                     messagebox.showerror('Error', 'Invalid Phone number', parent=first)
                                      else:
                                           messagebox.showerror('Error', 'Full Name must be String Character',
                                                                parent=first)
                            
                            ########################################## To Display the data of student ######################################

                            def display():
                                conn = pymysql.connect(host="localhost", user="root", password="",
                                                       database="recognition")
                                cur = conn.cursor()
                                cur.execute("select * from attendance")
                                data = cur.fetchall()
                                if len(data) != 0:
                                    table1.delete(*table1.get_children())
                                    for row in data:
                                        table1.insert('', END, values=row)
                                    conn.commit()
                                conn.close()

                            ########################################### To clear the data ###################################################
                            def clear():
                                eid_var.set("")
                                post_var.set("")
                                fname_var.set("")
                                gender_var.set("")
                                contact_var.set("")
                                address_var.set("")
                                guardian_name_var.set("")
                                guardian_email_var.set("")
                                guardian_contact_var.set("")

                            ##################################### To display the selected items in text field area ##################################
                            def focus_data(event):
                                cursor = table1.focus()
                                contents = table1.item(cursor)
                                row = contents['values']
                                if (len(row) != 0):
                                    eid_var.set(row[0])
                                    post_var.set(row[1])
                                    fname_var.set(row[2])
                                    gender_var.set(row[3])
                                    contact_var.set(row[4])
                                    address_var.set(row[5])
                                    guardian_name_var.set(row[6])
                                    guardian_email_var.set(row[7])
                                    guardian_contact_var.set(row[8])

                            ############################################## To update the data  ################################################
                            def update():
                                conn = pymysql.connect(host="localhost", user="root", password="",
                                                       database="recognition")
                                cur = conn.cursor()
                                if post_var.get() == "" or fname_var.get() == "" or gender_var.get() == "" or contact_var.get() == "" or address_var.get() == "":
                                    messagebox.showerror("Error", "All fields are Required", parent=first)
                                else:
                                    if (re.search('[a-zA-Z]+', fname_var.get())):
                                        if len(contact_var.get()) != 10:
                                            messagebox.showerror('Error', 'Contact Number must be 10 digits',
                                                                 parent=first)
                                        else:
                                            if (re.search('^[9]\d{9}$', contact_var.get())):
                                                regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
                                                if (re.search(regex, address_var.get())):
                                                    id = eid_var.get()
                                                    name = fname_var.get()
                                                    student_names = os.listdir(dataset_dir)
                                                    student_ids = [x.split('_')[1] for x in student_names]
                                                    if id in student_ids:
                                                        index = student_ids.index(id)
                                                        student_name = student_names[index]
                                                        q = messagebox.askyesno("Notification",
                                                                                "Do you want to update the photo samples too",
                                                                                parent=attendance)
                                                        if (q == True):
                                                            input_directory = os.path.join(dataset_dir, student_name)
                                                            shutil.rmtree(input_directory)
                                                            output_directory = os.path.join(dataset_dir,
                                                                                            name + "_" + id)
                                                            os.mkdir(output_directory)
                                                            count = 1
                                                            print("[INFO] starting video stream...")
                                                            video_capture = cv2.VideoCapture(1)
                                                            while count <= 100:
                                                                try:
                                                                    check, frame = video_capture.read()
                                                                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                                                                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                                                                    for (x, y, w, h) in faces:
                                                                        face = frame[y - 5:y + h + 5, x - 5:x + w + 5]
                                                                        resized_face = cv2.resize(face, (160, 160))
                                                                        cv2.imwrite(os.path.join(output_directory,
                                                                                                 name + str(
                                                                                                     count) + '.jpg'),
                                                                                    resized_face)
                                                                        cv2.rectangle(frame, (x, y), (x + w, y + h),
                                                                                      (0, 0, 255), 2)
                                                                        count += 1

                                                                    # show the output frame
                                                                    cv2.imshow("Frame", frame)
                                                                    key = cv2.waitKey(1)
                                                                    if key == ord('q'):
                                                                        break
                                                                except Exception as e:
                                                                    pass
                                                            video_capture.release()
                                                            cv2.destroyAllWindows()
                                                            cur.execute(
                                                                "update attendance set department = %s, fname = %s, gender = %s, contact_no = %s, email_address = %s, guardian_name = %s, guardian_email = %s, guardian_contact = %s where eid = %s",
                                                                (
                                                                    post_var.get(),
                                                                    fname_var.get(),
                                                                    gender_var.get(),
                                                                    contact_var.get(),
                                                                    address_var.get(),
                                                                    guardian_name_var.get(),
                                                                    guardian_email_var.get(),
                                                                    guardian_contact_var.get(),
                                                                    eid_var.get()
                                                                ))
                                                            conn.commit()
                                                            display()
                                                            clear()
                                                            conn.close()
                                                            messagebox.showinfo("Success",
                                                                                "Photos and database updated successfully",
                                                                                parent=first)

                                                        else:
                                                            os.rename(os.path.join(dataset_dir, student_name),
                                                                      os.path.join(dataset_dir, name + "_" + id))
                                                            cur.execute(
                                                                "update attendance set department = %s, fname = %s, gender = %s, contact_no = %s, email_address = %s, guardian_name = %s, guardian_email = %s, guardian_contact = %s where eid = %s",
                                                                (
                                                                    post_var.get(),
                                                                    fname_var.get(),
                                                                    gender_var.get(),
                                                                    contact_var.get(),
                                                                    address_var.get(),
                                                                    guardian_name_var.get(),
                                                                    guardian_email_var.get(),
                                                                    guardian_contact_var.get(),
                                                                    eid_var.get()
                                                                ))
                                                            conn.commit()
                                                            display()
                                                            clear()
                                                            conn.close()
                                                            messagebox.showinfo("Success",
                                                                                "Database updated successfully",
                                                                                parent=first)
                                                    else:
                                                        ques = messagebox.askyesno("Notification",
                                                                                   "Photo samples for this student did not exist in local directory. Please delete the entry from the database",
                                                                                   parent=attendance)
                                                        if (ques == True):
                                                            delete()
                                                            messagebox.showinfo("Success",
                                                                                "Database Updated successfully")
                                                        else:
                                                            delete()
                                                            messagebox.showinfo("Success",
                                                                                "Database Updated successfully")
                                                else:
                                                    messagebox.showerror('Error',
                                                                         'Please Enter the Valid Email Address',
                                                                         parent=first)
                                            else:
                                                messagebox.showerror('Error', 'Invalid Contact number', parent=first)
                                    else:
                                        messagebox.showerror('Error', 'Full Name must be String Character',
                                                             parent=first)

                            ################################################# To delete the items ###################################################
                            def delete():
                                conn = pymysql.connect(host="localhost", user="root", password="",
                                                       database="recognition")
                                cur = conn.cursor()
                                if post_var.get() == "" or fname_var.get() == "" or gender_var.get() == "" or contact_var.get() == "" or address_var.get() == "":
                                    messagebox.showerror("Error", "All fields are Required", parent=first)
                                else:
                                    try:
                                        input_name = fname_var.get() + "_" + eid_var.get()
                                        student_input = os.path.join(dataset_dir, input_name)
                                        if not os.path.exists(student_input):
                                            cur.execute("delete from attendance where eid = %s", eid_var.get())
                                        else:
                                            cur.execute("delete from attendance where eid = %s", eid_var.get())
                                            shutil.rmtree(student_input)
                                        conn.commit()
                                        conn.close()
                                        display()
                                        clear()
                                    except Exception as e:
                                        messagebox.showerror("Error", e)

                            def search_data():
                                conn = pymysql.connect(host="localhost", user="root", password="",
                                                       database="recognition")
                                cur = conn.cursor()
                                cur.execute(
                                    "select * from attendance where " + str(search_from.get()) + " LIKE '%" + str(
                                        search_result.get()) + "%'")
                                data = cur.fetchall()
                                if len(data) != 0:
                                    table1.delete(*table1.get_children())
                                    for row in data:
                                        table1.insert('', END, values=row)
                                    conn.commit()
                                else:
                                    messagebox.showinfo('Sorry', 'No Data Found', parent=first)
                                conn.close()

                            def show_data():
                                display()

                                ################################################## student Management form ###################################

                            f2 = Frame(first, bg="#202020", borderwidth="3", relief=SUNKEN, height=740, width=420)
                            titles = Label(f2, text="Add Student", fg="white", bg="#202020",
                                           font=("Helvetica", 20, "bold")).place(x=90, y=30)
                            id = Label(f2, text="Student ID", fg="white", bg="#202020",
                                       font=("Helvetica", 13, "bold")).place(x=35, y=100)
                            E1 = Entry(f2, state="disabled", width=20, textvariable=eid_var,
                                       font=("italic", 13, "bold")).place(x=35, y=130)
                            post = Label(f2, text="Year", fg="white", bg="#202020",
                                         font=("Helvetica", 13, "bold")).place(x=35, y=160)
                            E2 = Entry(f2, width=20, textvariable=post_var, font=("italic", 13, "bold")).place(x=35,
                                                                                                               y=190)
                            name = Label(f2, text="Full Name", fg="white", bg="#202020",
                                         font=("Helvetica", 13, "bold")).place(x=35, y=220)
                            E3 = Entry(f2, width=20, textvariable=fname_var, font=("italic", 12, "bold")).place(x=35,
                                                                                                                y=250)
                            gender = Label(f2, text="Gender", fg="white", bg="#202020",
                                           font=("Helvetica", 12, "bold")).place(x=35, y=280)
                            E7 = Combobox(f2, textvariable=gender_var, values=["Male", "Female", "Others"],
                                          state="readonly", font=("italic", 11, "bold")).place(x=35, y=310)
                            no = Label(f2, text="Contact.No", fg="white", bg="#202020",
                                       font=("Helvetica", 12, "bold")).place(x=35, y=340)
                            E4 = Entry(f2, width=20, textvariable=contact_var, font=("Helvetica", 12, "bold")).place(
                                x=35, y=370)
                            address = Label(f2, text=" Email Address", fg="white", bg="#202020",
                                            font=("Helvetica", 12, "bold")).place(x=35, y=400)
                            E5 = Entry(f2, width=20, textvariable=address_var, font=("italic", 12, "bold")).place(x=35,
                                                                                                                  y=430)
                            # Guardian Information
                            guardian_name_label = Label(f2, text="Guardian Name", fg="white", bg="#202020",
                                                        font=("Helvetica", 12, "bold")).place(x=35, y=460)
                            E6 = Entry(f2, width=20, textvariable=guardian_name_var, font=("italic", 12, "bold")).place(
                                x=35,
                                y=490)
                            guardian_email_label = Label(f2, text="Guardian Email", fg="white", bg="#202020",
                                                         font=("Helvetica", 12, "bold")).place(x=35, y=520)
                            E8 = Entry(f2, width=20, textvariable=guardian_email_var,
                                       font=("italic", 12, "bold")).place(x=35,
                                                                          y=550)
                            guardian_contact_label = Label(f2, text="Guardian Contact", fg="white", bg="#202020",
                                                           font=("Helvetica", 12, "bold")).place(x=35, y=580)
                            E9 = Entry(f2, width=20, textvariable=guardian_contact_var,
                                       font=("italic", 12, "bold")).place(x=35,
                                                                          y=610)

                            f2.place(x=10, y=20)
                            # b2 = Button(first, text = "Close", command = first.destroy ).place(x = 135, y = 600)
                            f3 = Frame(first, bg="#202020", height=60, width=402)
                            btn1 = Button(f3, text="Add", bg="#FF9900", height="1", width="7", command=add_student,
                                          font=("Helvetica", 14, "bold")).place(x=5, y=10)
                            btn2 = Button(f3, text="Update", bg="#FF9900", height="1", width="7", command=update,
                                          font=("Helvetica", 14, "bold")).place(x=105, y=10)
                            btn3 = Button(f3, text="Delete", bg="#FF9900", height="1", width="7", command=delete,
                                          font=("Helvetica", 14, "bold")).place(x=205, y=10)
                            btn4 = Button(f3, text="Clear", bg="#FF9900", height="1", width="7", command=clear,
                                          font=("Helvetica", 14, "bold")).place(x=305, y=10)
                            # btn5 = Button(f3, text = "Add Photo Sample", bg = "yellow", height = "2", width = "34",command = add_photo, font = ("Times new Roman", 14 , "bold")).place(x = 10, y = 60)
                            f3.place(x=20, y=690)

                            ########################################## Large Frame ###########################################################
                            f4 = Frame(first, height=740, width=1090, bg="#202020", borderwidth="3", relief=SUNKEN)
                            f4.place(x=440, y=18)
                            l1 = Label(first, text="Search By:", font=("Helvetica", 18, "bold"), bg="#202020",
                                       fg="white").place(x=460, y=25)
                            c1 = Combobox(first, textvariable=search_from, values=["eid", "fname", "post"],
                                          state="readonly", width="25").place(x=600, y=29)
                            E7 = Entry(first, textvariable=search_result, width="25", font=("Helvetica", 10)).place(
                                x=800, y=29)
                            btn7 = Button(first, text="Search ", height="1", width="12", command=search_data,
                                          font=("Helvetica", 13, "bold")).place(x=990, y=25)
                            btn8 = Button(first, text="Show All", height="1", width="12", command=show_data,
                                          font=("Helvetica", 13, "bold")).place(x=1180, y=25)

                            ########################################## Table frame ###########################################################
                            f5 = Frame(f4, bg="#202020", borderwidth="2", relief=SUNKEN)
                            f5.place(x=20, y=45, height=670, width=1050)
                            scroll_x = Scrollbar(f5, orient=HORIZONTAL)
                            scroll_y = Scrollbar(f5, orient=VERTICAL)
                            table1 = Treeview(f5, columns=(
                                "eid", "post", "fname", "gender", "contact.no", "address", "guardian_name",
                                "guardian_email", "guardian_contact", "DOJ"),
                                              xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
                            scroll_x.pack(side=BOTTOM, fill=X)
                            scroll_y.pack(side=RIGHT, fill=Y)
                            scroll_x.config(command=table1.xview)
                            scroll_y.config(command=table1.yview)
                            table1.heading("eid", text="Student ID")
                            table1.heading('post', text="Year")
                            table1.heading("fname", text="Full Name")
                            table1.heading("gender", text="Gender")
                            table1.heading("contact.no", text="Contact_No")
                            table1.heading("address", text=" Email Address")
                            table1.heading("guardian_name", text="Guardian Name")
                            table1.heading("guardian_email", text="Guardian Email")
                            table1.heading("guardian_contact", text="Guardian Contact")
                            table1.heading("DOJ", text="Date Of Join")

                            table1['show'] = 'headings'
                            table1.column("eid", width=100)
                            table1.column("post", width=100)
                            table1.column("fname", width=100)
                            table1.column("gender", width=100)
                            table1.column("contact.no", width=100)
                            table1.column("address", width=100)
                            table1.column("guardian_name", width=100)
                            table1.column("guardian_email", width=100)
                            table1.column("guardian_contact", width=100)
                            table1.column("DOJ", width=100)
                            table1.pack(fill=BOTH, expand=1)
                            table1.bind("<ButtonRelease-1>", focus_data)
                            display()
                            first.mainloop()
                        except pymysql.err.OperationalError as e:
                            messagebox.showerror("Error",
                                                 "Sql Connection Error... Open Xamp Control Panel and then start MySql Server ")
                        except Exception as e:
                            print(e)
                            messagebox.showerror("Error", "Close all the windows and restart your program")

                    def train():
                        try:
                            second = Toplevel()
                            second.title("Train The System")
                            second.geometry("1400x700+0+0")
                            second.configure(bg="#202020")
                            train_title = Label(second, text="Train the System", fg='white',
                                                font=("Helvetica", 20, "bold"), bg="#202020")
                            train_title.place(x=0, y=0, relwidth=1)

                            def back():
                                second.destroy()

                            backbtn = Button(second, text='Back', fg='black', bg='white', font=('Helvetica', 15),
                                             height=1, width=7, command=back)
                            backbtn.place(x=1260, y=3)

                            def progress():
                                progress_bar.start(5)
                                try:
                                    training_obj = Training(embedding_path='models/embeddings.pickle')
                                    label_encoder, labels, embeddings, ids = training_obj.load_embeddings_and_labels()

                                    print("Length of ids:", len(ids))
                                    print("Length of labels:", len(labels))
                                    print("Length of embeddings:", len(embeddings))

                                    # Ensure that each label has a corresponding embedding
                                    unique_labels = set(labels)
                                    filtered_labels = []
                                    filtered_embeddings = []
                                    for label in unique_labels:
                                        indices = [i for i, l in enumerate(labels) if l == label]
                                        filtered_labels.extend([label] * len(indices))
                                        filtered_embeddings.extend([embeddings[i] for i in indices])

                                    # Convert filtered labels to numpy array
                                    filtered_labels = np.array(filtered_labels)

                                    recognizer = training_obj.create_svm_model(filtered_labels, filtered_embeddings)
                                    with open('models/recognizer.pickle', "wb") as f1:
                                        pickle.dump(recognizer, f1)

                                    messagebox.showinfo("Success",
                                                        "Training Done Successfully. New pickle file created to store Face Recognition Model",
                                                        parent=second)
                                    second.after(1000, second.destroy)
                                except FileNotFoundError as e:
                                    second.after(1000, second.destroy)
                                    messagebox.showerror("Error",
                                                         f"Pickle file for embeddings is missing. {str(e).split(':')[-1]} not found. First Extract Embeddings and then try again")
                                except ValueError as e:
                                    second.after(1000, second.destroy)
                                    messagebox.showerror("Error", str(e))
                                except Exception as e:
                                    second.after(1000, second.destroy)
                                    messagebox.showerror("Error", f"{e} not found.")

                            progress_bar = Progressbar(second, orient=HORIZONTAL, length=500, mode='determinate')
                            progress_bar.place(x=430, y=520)
                            btn = Button(second, text="Start Training", fg='white', font=("Helvetica", 20, "bold"),
                                         command=progress, bg="#FF9900")
                            btn.place(x=600, y=450)
                            second.mainloop()
                        except Exception as e:
                            second.after(1000, second.destroy)
                            messagebox.showerror("Error", "{} not found.".format(e))

                    def Logintrain():
                        try:
                            second = Toplevel()
                            second.title("Train The System")
                            second.geometry("1400x700+0+0")
                            second.configure(bg="#202020")
                            train_title = Label(second, text="Train the System", fg='white',
                                                font=("Helvetica", 20, "bold"), bg="#202020")
                            train_title.place(x=0, y=0, relwidth=1)

                            def back():
                                second.destroy()

                            backbtn = Button(second, text='Back', fg='black', bg='white', font=('Helvetica', 15),
                                             height=1, width=7, command=back)
                            backbtn.place(x=1260, y=3)

                            def progress():
                                progress_bar.start(5)
                                try:
                                    embedding_path = os.path.join('models', 'login_embeddings.pickle')

                                    # Training for face login recognizer
                                    face_login_training_obj = LoginTraining(embedding_path=embedding_path,
                                                                            recognizer_type='login')
                                    [label, labels, Embeddings,
                                     usernames] = face_login_training_obj.load_embeddings_and_labels()
                                    face_login_recognizer = face_login_training_obj.create_svm_model(labels=labels,
                                                                                                     embeddings=Embeddings)
                                    face_login_training_obj.save_recognizer(face_login_recognizer)

                                    # Training for face attendance recognizer

                                    messagebox.showinfo("Success",
                                                        "Training Done Successfully. New pickle files created to store Face Login and Face Attendance Recognizers",
                                                        parent=second)
                                    second.after(1000, second.destroy)
                                except FileNotFoundError as e:
                                    second.after(1000, second.destroy)
                                    messagebox.showerror("Error",
                                                         f"Pickle file for embeddings is missing. {str(e).split(':')[-1]} not found. First Extract Embeddings and then try again")
                                except ValueError as e:
                                    second.after(1000, second.destroy)
                                    messagebox.showerror("Error", str(e))
                                except Exception as e:
                                    second.after(1000, second.destroy)
                                    messagebox.showerror("Error", f"{e} not found.")

                            progress_bar = Progressbar(second, orient='horizontal', length=500, mode='determinate')
                            progress_bar.place(x=430, y=520)
                            btn = Button(second, text="Start Training", fg='white', font=("Helvetica", 20, "bold"),
                                         command=progress, bg="#FF9900")
                            btn.place(x=600, y=450)
                            second.mainloop()
                        except Exception as e:
                            second.after(1000, second.destroy)
                            messagebox.showerror("Error", f"{e} not found.")

                    ######################################## email automation ######################
                    
                    def trigger_email ():
                         try:
                              # Define the directory to store user trigger files
                              user_trigger_dir = "user_triggers"
                              if not os.path.exists(user_trigger_dir):
                                   os.makedirs(user_trigger_dir)
                              
                              # Define the path to the user's trigger file
                              user_trigger_file = os.path.join(user_trigger_dir, f"{logged_in_username}.txt")
                              
                              # Check if the user has triggered the email before
                              if os.path.exists(user_trigger_file):
                                   # Read the last trigger time from the user's trigger file
                                   with open(user_trigger_file, "r") as f:
                                        last_trigger_time_str = f.read().strip()
                                   last_trigger_time = datetime.strptime(last_trigger_time_str, "%Y-%m-%d %H:%M:%S")
                                   # Check if it's been more than 24 hours since the last trigger
                                   if datetime.now() - last_trigger_time < timedelta(hours=24):
                                        messagebox.showinfo("Information", "Email already sent in the last 24 hours.")
                                        return
                              else:
                                   # If the user's trigger file doesn't exist, create it and write the current time
                                   with open(user_trigger_file, "w") as f:
                                        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                              
                              # Call the send_mail function
                              send_mail()
                              
                              # Update the last trigger time in the user's trigger file
                              with open(user_trigger_file, "w") as f:
                                   f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                              
                              messagebox.showinfo("Success", "Email sent successfully!")
                         except Exception as e:
                              messagebox.showerror("Error", f"An error occurred: {str(e)}")

        ######################################### Function to recognize the face #######################################

                    def distance(emb1, emb2):
                        return np.sqrt(np.square(emb1 - emb2))

                    def getkey(val, student_details):
                        for key, value in student_details.items():
                            if val == value:
                                return key
                        return "Unknown"

                    def time_in():
                        start_time = datetime.now()
                        embeddings_model_file = os.path.join(root_dir, "models/embeddings.pickle")
                        recognizer_model_file = os.path.join(root_dir, "models/recognizer.pickle")
                        predictions = []
                        spoof_attempts = []
                        liveness_predictor = []
                        detection_counter = 0  # Counter to track the number of detections
                        # Check if model files exist
                        if os.path.exists(embeddings_model_file) and os.path.exists(recognizer_model_file):
                            try:
                                # Load embeddings and labels
                                training_obj = Training(embedding_path='models/embeddings.pickle')
                                [label, labels, Embeddings, ids] = training_obj.load_embeddings_and_labels()
                                student_details = embedding_obj.get_student_details()
                                # Load recognizer model
                                recognizer = pickle.loads(open('models/recognizer.pickle', "rb").read())
                                # Start video stream
                                vs = cv2.VideoCapture(1)
                                print("[INFO] starting video stream...")
                                window_name = "Frameless Window"
                                cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                                # Set window flags to remove the title bar
                                cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                                cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_GUI_NORMAL)
                                # Set the initial position
                                cv2.moveWindow(window_name, 400, 130)
                                # Set fixed size
                                cv2.resizeWindow(window_name, 700, 460)
                            except Exception as e:
                                # Display error message
                                messagebox.showerror("Error", e)
                                return

                            # Main loop for face recognition
                            while True:
                                try:
                                    # Capture frame from video stream
                                    (ret, frame) = vs.read()
                                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                                    # Detect faces in the frame
                                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                                    # Loop through detected faces
                                    for (x, y, w, h) in faces:
                                        # Extract face region
                                        face = frame[y - 5:y + h + 5, x - 5:x + w + 5]
                                        resized_face = cv2.resize(face, (160, 160))
                                        # Preprocess face for prediction
                                        processed_face = resized_face.astype("float") / 255.0
                                        processed_face = img_to_array(processed_face)
                                        processed_face = np.expand_dims(processed_face, axis=0)
                                        # Predict liveness of the face
                                        preds = liveness_model.predict(processed_face)[0]
                                        text = "UNKNOWN"
                                        # Determine label color based on liveness prediction
                                        if preds > 0.9:  # Spoofing
                                            label_name = 'spoof'
                                            color = (0, 0, 255)  # Red color for spoofing
                                            spoof_attempts.append((x, y, w, h))  # Record spoof attempts
                                            text = "SPOOF ATTEMPT"
                                        elif preds < 0.5:  # Real person
                                            label_name = "real"
                                            color = (0, 255, 0)  # Green color for real person
                                            detection_counter += 1  # Increment the detection counter
                                            if label_name == "real":  # Check if it's a real person
                                                # Normalize pixels and predict embedding
                                                face_pixel = embedding_obj.normalize_pixels(
                                                    imagearrays=resized_face)
                                                sample = np.expand_dims(face_pixel, axis=0)
                                                embedding = embedding_model.predict(sample)
                                                embedding = embedding.reshape(1, -1)
                                                # Recognize face using the recognizer model
                                                preds = recognizer.predict_proba(embedding)[0]
                                                p = np.argmax(preds)
                                                proba = preds[p]
                                                if proba > 0.8:  # Confidence threshold for recognition
                                                    id = label.classes_[p]
                                                    name = getkey(id, student_details)
                                                    # Fetch department data from the database
                                                    cur = conn.cursor()
                                                    cur.execute("SELECT department FROM attendance WHERE eid = %s",
                                                                (id,))
                                                    department_result = cur.fetchone()
                                                    department = department_result[
                                                        0] if department_result else "Unknown"
                                                    text = "{} {} - {}".format(name, id, department)
                                                    predictions.append(id)
                                            else:
                                                text = "UNKNOWN"
                                                color = (255, 0, 0)
                                                # Display "UNKNOWN" for unrecognized real persons
                                        else:  # None
                                            label_name = "none"
                                            color = (255, 0, 0)  # Blue color for none
                                            if label_name != "spoof":  # Only set text to "UNKNOWN" if it's not a spoof attempt
                                                text = "UNKNOWN"
                                        # Update liveness predictor list
                                        liveness_predictor.append(label_name)
                                        # Determine text to display on frame
                                        if label_name != "spoof":
                                            if label_name == "real":
                                                # Normalize pixels and predict embedding
                                                face_pixel = embedding_obj.normalize_pixels(
                                                    imagearrays=resized_face)
                                                sample = np.expand_dims(face_pixel, axis=0)
                                                embedding = embedding_model.predict(sample)
                                                embedding = embedding.reshape(1, -1)
                                                # Recognize face using the recognizer model
                                                preds = recognizer.predict_proba(embedding)[0]
                                                p = np.argmax(preds)
                                                proba = preds[p]
                                                if proba > 0.8:  # Confidence threshold for recognition
                                                    id = label.classes_[p]
                                                    name = getkey(id, student_details)
                                                    # Fetch department data from the database
                                                    cur = conn.cursor()
                                                    cur.execute("SELECT department FROM attendance WHERE eid = %s",
                                                                (id,))
                                                    department_result = cur.fetchone()
                                                    department = department_result[
                                                        0] if department_result else "Unknown"
                                                    text = "{} {} - {}".format(name, id, department)
                                                    predictions.append(id)
                                        # Draw rectangle and put text on the frame
                                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                                        cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color,
                                                    2)
                                    # Display frame in OpenCV window
                                    cv2.imshow(window_name, frame)
                                    key = cv2.waitKey(1) & 0xFF
                                    if key == ord('q'):
                                        break
                                except Exception as e:
                                    # Display error message
                                    messagebox.showerror("Error", e)
                                    break
                            # Release video stream and close OpenCV windows
                            vs.release()
                            cv2.destroyAllWindows()

                            # Remaining code for attendance recording...
                            # Remaining code for attendance recording...
                            all_student_ids = set(student_details.values())
                            # Find out which students didn't scan
                            students_absent = all_student_ids - set(predictions)

                            if detection_counter >= 10:
                                # Record attendance for the detected real person
                                for final_id in set(predictions):
                                    final_name = getkey(final_id, student_details)
                                    print(final_name)
                                    print(final_id)

                                    late_threshold = 600
                                    absent_threshold = 900

                                    time_difference = (datetime.now() - start_time).total_seconds()
                                    print("Time Difference:", time_difference)

                                    if time_difference <= late_threshold:
                                        status = "Present"
                                    elif late_threshold < time_difference <= absent_threshold:
                                        status = "Late"
                                    else:
                                        status = "Absent"

                                    print("Late Threshold:", late_threshold)
                                    print("Absent Threshold:", absent_threshold)
                                    print("Status:", status)

                                    # Show info messagebox for attendance status
                                    messagebox.showinfo("Attendance Status",
                                                        "Hello {}. Your attendance is recorded as {}.".format(
                                                            final_name, status))

                                    # Fetch department data from the database
                                    cur = conn.cursor()
                                    cur.execute("SELECT department FROM attendance WHERE eid = %s", (final_id,))
                                    department_result = cur.fetchone()
                                    department = department_result[0] if department_result else "Unknown"

                                    # Fetch subject data for the logged-in user
                                    cur.execute("SELECT subject FROM login WHERE username = %s", (logged_in_username,))
                                    subject_result = cur.fetchone()
                                    subject = subject_result[0] if subject_result else "Unknown"

                                    # Insert attendance record into report
                                    cur2 = conn.cursor()
                                    cur2.execute(
                                        "INSERT INTO report(id, name, department, subject, date, time, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                        (final_id, final_name, department, subject, date.today(),
                                         datetime.now().strftime("%H:%M:%S"),
                                         status))
                                    conn.commit()

                            # Handle students who didn't scan but should be marked as absent
                            for absent_id in students_absent:
                                absent_name = getkey(absent_id, student_details)
                                print(absent_name)
                                print(absent_id)

                                absent_threshold = 1

                                time_difference = (datetime.now() - start_time).total_seconds()
                                print("Time Difference:", time_difference)

                                if time_difference > absent_threshold:
                                    status = "Absent"

                                    # Fetch department data from the database
                                    cur = conn.cursor()
                                    cur.execute("SELECT department FROM attendance WHERE eid = %s", (absent_id,))
                                    department_result = cur.fetchone()
                                    department = department_result[0] if department_result else "Unknown"

                                    # Fetch subject data for the logged-in user
                                    cur.execute("SELECT subject FROM login WHERE username = %s", (logged_in_username,))
                                    subject_result = cur.fetchone()
                                    subject = subject_result[0] if subject_result else "Unknown"

                                    # Insert attendance record into report
                                    cur2 = conn.cursor()
                                    cur2.execute(
                                        "INSERT INTO report(id, name, department, subject, date, time, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                        (absent_id, absent_name, department, subject, date.today(),
                                         datetime.now().strftime("%H:%M:%S"),
                                         status))
                                    conn.commit()

                                    # Show info messagebox for attendance status
                                  

                            # Display spoof attempts
                            if spoof_attempts:
                                messagebox.showinfo("Spoof Attempts Detected",
                                                    "Spoof attempts detected. No attendance recorded for these attempts.")

                                cv2.destroyAllWindows()

                            

                        else:
                            messagebox.showerror("Error",
                                                 "Model files not found. Embeddings.pickle file and Recognizer.pickle file must exist within models directory.")

                    def time_out():
                        start_time = datetime.now()
                        embeddings_model_file = os.path.join(root_dir, "models/embeddings.pickle")
                        recognizer_model_file = os.path.join(root_dir, "models/recognizer.pickle")
                        predictions = []
                        spoof_attempts = []
                        liveness_predictor = []
                        detection_counter = 0  # Counter to track the number of detections

                        # Check if model files exist
                        if os.path.exists(embeddings_model_file) and os.path.exists(recognizer_model_file):
                            try:
                                # Load embeddings and labels
                                training_obj = Training(embedding_path='models/embeddings.pickle')
                                [label, labels, Embeddings, ids] = training_obj.load_embeddings_and_labels()
                                student_details = embedding_obj.get_student_details()

                                # Load recognizer model
                                recognizer = pickle.loads(open('models/recognizer.pickle', "rb").read())

                                # Start video stream
                                vs = cv2.VideoCapture(1)
                                print("[INFO] starting video stream...")
                                window_name = "Frameless Window"
                                cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

                                # Set window flags to remove the title bar
                                cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                                cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_GUI_NORMAL)

                                # Set the initial position
                                cv2.moveWindow(window_name, 400, 130)

                                # Set fixed size
                                cv2.resizeWindow(window_name, 700, 460)
                            except Exception as e:
                                # Display error message
                                messagebox.showerror("Error", e)
                                return

                            # Main loop for face recognition
                            while True:
                                try:
                                    # Capture frame from video stream
                                    (ret, frame) = vs.read()
                                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                                    # Detect faces in the frame
                                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                                    # Loop through detected faces
                                    for (x, y, w, h) in faces:
                                        # Extract face region
                                        face = frame[y - 5:y + h + 5, x - 5:x + w + 5]
                                        resized_face = cv2.resize(face, (160, 160))

                                        # Preprocess face for prediction
                                        processed_face = resized_face.astype("float") / 255.0
                                        processed_face = img_to_array(processed_face)
                                        processed_face = np.expand_dims(processed_face, axis=0)

                                        # Predict liveness of the face
                                        preds = liveness_model.predict(processed_face)[0]
                                        text = "UNKNOWN"
                                        # Determine label color based on liveness prediction
                                        if preds > 0.9:  # Spoofing
                                            label_name = 'spoof'
                                            color = (0, 0, 255)  # Red color for spoofing
                                            spoof_attempts.append((x, y, w, h))  # Record spoof attempts
                                            text = "SPOOF ATTEMPT"
                                        elif preds < 0.5:  # Real person
                                            label_name = "real"
                                            color = (0, 255, 0)  # Green color for real person
                                            detection_counter += 1  # Increment the detection counter
                                            if label_name == "real":  # Check if it's a real person
                                                # Normalize pixels and predict embedding
                                                face_pixel = embedding_obj.normalize_pixels(
                                                    imagearrays=resized_face)
                                                sample = np.expand_dims(face_pixel, axis=0)
                                                embedding = embedding_model.predict(sample)
                                                embedding = embedding.reshape(1, -1)

                                                # Recognize face using the recognizer model
                                                preds = recognizer.predict_proba(embedding)[0]
                                                p = np.argmax(preds)
                                                proba = preds[p]
                                                if proba > 0.8:  # Confidence threshold for recognition
                                                    id = label.classes_[p]
                                                    name = getkey(id, student_details)

                                                    # Fetch department data from the database
                                                    cur = conn.cursor()
                                                    cur.execute("SELECT department FROM attendance WHERE eid = %s",
                                                                (id,))
                                                    department_result = cur.fetchone()
                                                    department = department_result[
                                                        0] if department_result else "Unknown"

                                                    text = "{} {} - {}".format(name, id, department)
                                                    predictions.append(id)
                                            else:
                                                text = "UNKNOWN"
                                                color = (255, 0, 0)
                                                # Display "UNKNOWN" for unrecognized real persons
                                        else:  # None
                                            label_name = "none"
                                            color = (255, 0, 0)  # Blue color for none
                                            if label_name != "spoof":  # Only set text to "UNKNOWN" if it's not a spoof attempt
                                                text = "UNKNOWN"

                                        # Update liveness predictor list
                                        liveness_predictor.append(label_name)

                                        # Determine text to display on frame
                                        if label_name != "spoof":
                                            if label_name == "real":
                                                # Normalize pixels and predict embedding
                                                face_pixel = embedding_obj.normalize_pixels(
                                                    imagearrays=resized_face)
                                                sample = np.expand_dims(face_pixel, axis=0)
                                                embedding = embedding_model.predict(sample)
                                                embedding = embedding.reshape(1, -1)

                                                # Recognize face using the recognizer model
                                                preds = recognizer.predict_proba(embedding)[0]
                                                p = np.argmax(preds)
                                                proba = preds[p]
                                                if proba > 0.8:  # Confidence threshold for recognition
                                                    id = label.classes_[p]
                                                    name = getkey(id, student_details)

                                                    # Fetch department data from the database
                                                    cur = conn.cursor()
                                                    cur.execute("SELECT department FROM attendance WHERE eid = %s",
                                                                (id,))
                                                    department_result = cur.fetchone()
                                                    department = department_result[
                                                        0] if department_result else "Unknown"

                                                    text = "{} {} - {}".format(name, id, department)
                                                    predictions.append(id)

                                        # Draw rectangle and put text on the frame
                                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                                        cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color,
                                                    2)

                                    # Display frame in OpenCV window
                                    cv2.imshow(window_name, frame)
                                    key = cv2.waitKey(1) & 0xFF
                                    if key == ord('q'):
                                        break

                                except Exception as e:
                                    # Display error message
                                    messagebox.showerror("Error", e)
                                    break

                            # Release video stream and close OpenCV windows
                            vs.release()
                            cv2.destroyAllWindows()

                            # Remaining code for attendance recording...
                            if detection_counter >= 10:
                                # Record attendance for the detected real person
                                if predictions:
                                    for final_id in set(predictions):
                                        final_name = getkey(final_id, student_details)
                                        print(final_name)
                                        print(final_id)

                                        late_threshold = 600
                                        absent_threshold = 900

                                        time_difference = (datetime.now() - start_time).total_seconds()
                                        print("Time Difference:", time_difference)

                                        if time_difference <= late_threshold:
                                            status = "Present"
                                        elif late_threshold < time_difference <= absent_threshold:
                                            status = "Late"
                                        else:
                                            status = "Absent"

                                        print("Late Threshold:", late_threshold)
                                        print("Absent Threshold:", absent_threshold)
                                        print("Status:", status)

                                        # Fetch department and subject data from the database
                                        cur = conn.cursor()
                                        cur.execute("SELECT department, subject FROM attendance WHERE eid = %s",
                                                    (final_id,))
                                        department_subject_result = cur.fetchone()
                                        department = department_subject_result[
                                            0] if department_subject_result else "Unknown"
                                        subject = department_subject_result[
                                            1] if department_subject_result else "Unknown"

                                        # Show attendance status message box
                                      

                                        # Check if the student has a record in time in
                                        cur.execute(
                                            "SELECT * FROM report WHERE id = %s AND date = %s AND status = 'Present'",
                                            (final_id, date.today()))
                                        existing_record = cur.fetchone()

                                        if existing_record:
                                            # If the student has a record in time in, update the time
                                            cur2 = conn.cursor()
                                            cur2.execute(
                                                "UPDATE report SET time = %s WHERE id = %s AND date = %s AND status = 'Present'",
                                                (datetime.now().strftime("%H:%M:%S"), final_id, date.today()))
                                            conn.commit()
                                        else:
                                            # If the student has no record in time in, mark them as absent
                                            cur2 = conn.cursor()
                                            cur2.execute(
                                                "INSERT INTO report(id, name, department, subject, date, time, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                                (final_id, final_name, department, subject, date.today(),
                                                 datetime.now().strftime("%H:%M:%S"),
                                                 "Absent"))
                                            conn.commit()

                            # Update attendance status for students who didn't scan during time out
                            all_student_ids = set(student_details.values())
                            students_absent_timeout = all_student_ids - set(predictions)
                            for absent_id in students_absent_timeout:
                                absent_name = getkey(absent_id, student_details)
                                absent_threshold = 1
                                time_difference = (datetime.now() - start_time).total_seconds()
                                if time_difference > absent_threshold:
                                    status = "Absent"
                                    cur = conn.cursor()
                                    cur.execute(
                                        "UPDATE report SET status=%s, time=%s WHERE id=%s AND date=%s AND status='Present'",
                                        (status, datetime.now().strftime("%H:%M:%S"), absent_id, date.today()))
                                    conn.commit()
                                   
                            # Update attendance status for students present during time in but not recorded during time out
                            students_present_timeout = set(predictions) - all_student_ids
                            for present_id in students_present_timeout:
                                present_name = getkey(present_id, student_details)
                                status = "Absent"
                                cur = conn.cursor()
                                cur.execute(
                                    "UPDATE report SET status=%s, time=%s WHERE id=%s AND date=%s AND status='Present'",
                                    (status, datetime.now().strftime("%H:%M:%S"), present_id, date.today()))
                                conn.commit()
                                

                         

                        else:
                            messagebox.showerror("Error",
                                                 "Model files not found. Embeddings.pickle file and Recognizer.pickle file must exist within models directory.")
                    
                   
                    
               
                    ##################################  Function to recognize the face #############################



                        ######################################## To display the attendance register report ##############################

                    def report():
                        report = Toplevel()
                        report.geometry("1380x660+0+0")
                        report.title("Attendance Report")
                        report.config(bg="#FF9900")

                        def back():
                            report.destroy()

                        ############################################ Functions of all buttons that are used in this report window #########################################################
                        ############################################## To fetch the data from the database and display it into the app table #############################

                        ########################################### To update the data  ################################################



                        def clear():
                            return True
                        
                        def export_to_excel ():
                             try:
                                  conn = pymysql.connect(host="localhost", user="root", password="",
                                                         database="recognition")
                                  cur = conn.cursor()
                                  
                                  # Fetch username and subject from the login table based on the logged-in username
                                  cur.execute("SELECT username, subject FROM login WHERE username = %s",
                                              (logged_in_username,))
                                  user_info = cur.fetchone()
                                  if user_info:
                                       username, subject = user_info
                                  else:
                                       username = "N/A"
                                       subject = "N/A"
                                  
                                  # Fetch data from the report table
                                  cur.execute("SELECT * FROM report")
                                  data = cur.fetchall()
                                  
                                  print("Fetched data:", data)  # Print fetched data for debugging
                                  
                                  if len(data) != 0:
                                       df = pd.DataFrame(data,
                                                         columns=['ID', 'Year', 'Name', 'Date', 'Time', 'Status',
                                                                  'Subject'])
                                       
                                       print("DataFrame created successfully.")  # Print message for debugging
                                       
                                       now = datetime.now()
                                       current_date_time = now.strftime("%Y_%m_%d_%H_%M")
                                       
                                       folder = 'exports'
                                       if not os.path.exists(folder):
                                            os.makedirs(folder)
                                       
                                       excel_filename = os.path.join(folder,
                                                                     f'attendance_report_Instructor_{logged_in_username}_Subject_{subject}_Date_created_{current_date_time}.xlsx')
                                       
                                       print("Excel filename:", excel_filename)  # Print filename for debugging
                                       
                                       df.to_excel(excel_filename, index=False)
                                       
                                       print("Excel file created successfully.")  # Print message for debugging
                                       
                                       messagebox.showinfo("Success",
                                                           f"Data has been exported to {excel_filename} successfully. Username: {username}, Subject: {subject}")
                                  else:
                                       messagebox.showinfo("Information", "No data found to export.")
                                  
                                  conn.close()
                             except Exception as e:
                                  messagebox.showerror("Error", f"An error occurred: {e}")
                        
                        # Creating the main application window

                        ##################################################### To show all the datas from the database #######################################################################
                        def show_data():
                            conn = pymysql.connect(host="localhost", user="root", password="", database="recognition")
                            cur = conn.cursor()
                            cur.execute("select * from report")
                            data = cur.fetchall()
                            if len(data) != 0:
                                report_table.delete(*report_table.get_children())
                                for row in data:
                                    report_table.insert('', END, values=row)
                                conn.commit()
                            conn.close()

                        ############################################ To save the csv data into mysql database ################################################################

                        def delete_data():
                            conn = pymysql.connect(host='localhost', user='root', password='', database='recognition')
                            cur = conn.cursor()
                            selected_item = report_table.selection()[0]
                            uid = report_table.item(selected_item)['values'][0]
                            print("UID is ", uid)
                            cur.execute('delete from report where id = %s', (uid))
                            conn.commit()
                            report_table.delete(selected_item)
                            messagebox.showinfo('Success', ' Data Deleted Successfully', parent=report)
                            conn.close()

                        def update(rows):
                            global mydata
                            mydata = rows
                            report_table.delete(*report_table.get_children())
                            for i in rows:
                                report_table.insert('', 'end', values=i)

                        def search_data():
                            conn = pymysql.connect(host="localhost", user="root", password="", database="recognition")
                            cur = conn.cursor()

                            cur.execute("select * from report where " + str(search_by.get()) + " LIKE '%" + str(
                                search_text.get()) + "%'")
                            rows = cur.fetchall()
                            if len(rows) != 0:
                                report_table.delete(*report_table.get_children())
                                for row in rows:
                                    report_table.insert('', END, values=row)
                                conn.commit()
                            else:
                                messagebox.showinfo('Sorry', 'No Data Found', parent=report)
                            conn.close()

                        search_by = StringVar()
                        search_text = StringVar()

                        ####################################### Textfill Frame ########################################
                        text_fill = Frame(report, height=640, width=1350, bg="#202020", borderwidth="3", relief=SUNKEN)
                        text_fill.place(x=10, y=10)
                        search_label = Label(text_fill, text="Search By:", fg="white", font=("Helvetica", 15, "bold"),
                                             bg="#202020")
                        search_label.place(x=10, y=13)
                        search_combo = Combobox(text_fill, textvariable=search_by, values=['date', 'name'],
                                                state='readonly', font=("times new roman", 15), width=12)
                        search_combo.place(x=150, y=13)
                        search_entry = Entry(text_fill, textvariable=search_text, font=("Helvetica", 15), width=12)
                        search_entry.place(x=330, y=13)
                        search_btn = Button(text_fill, text="Search", bg="#FF9900", fg="white",
                                            font=("Helvetica", 15, "bold"), command=search_data, width=12)
                        search_btn.place(x=530, y=10)
                        search_today = Button(text_fill, text="Delete", bg="#FF9900", fg="white",
                                              font=("Helvetica", 15, "bold"), command=delete_data, width=12)
                        search_today.place(x=730, y=10)
                        show_btn = Button(text_fill, height="1", text="Show All", bg="#FF9900", fg="white",
                                          font=("Helvetica", 15, "bold"), command=show_data, width=12)
                        show_btn.place(x=930, y=10)
                        excelbtn = Button(text_fill, height="1", text="Generate Excel", bg="#FF9900", fg="white",
                                          font=("Helvetica", 15, "bold"), command=export_to_excel, width=12)
                        excelbtn.place(x=1130, y=10)

                        ###################################### Table frame #######################################

                        table_frame = Frame(text_fill, borderwidth="3", relief=GROOVE, bg="white")
                        table_frame.place(x=10, y=55, height=560, width=1325)
                        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
                        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
                        report_table = Treeview(table_frame,
                                                columns=("ID", "Year", "Name", "Date", "Time", "Subject", "Status"),
                                                xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
                        scroll_x.pack(side=BOTTOM, fill=X)
                        scroll_y.pack(side=RIGHT, fill=Y)
                        scroll_x.config(command=report_table.xview)
                        scroll_y.config(command=report_table.yview)
                        report_table.heading('ID', text="ID")
                        report_table.heading('Year', text="Year")
                        report_table.heading('Date', text="Date")
                        report_table.heading('Name', text="Name")
                        report_table.heading("Time", text="Time")
                        report_table.heading("Subject", text="Subject")
                        report_table.heading("Status", text="Status")
                        report_table['show'] = 'headings'
                        report_table.column("ID", width=100)
                        report_table.column("Year", width=100)
                        report_table.column("Date", width=100)
                        report_table.column("Name", width=200)
                        report_table.column("Time", width=100)
                        report_table.column("Subject", width=200)
                        report_table.column("Status", width=100)
                        report_table.pack(fill=BOTH, expand=1)

                        show_data()
                        report.mainloop()

                    ################################## Function to exit the attendance management form ####################################
                    def exit():
                        ques = messagebox.askyesnocancel("Notification", "Do you Really want to exit?",
                                                         parent=attendance)
                        if (ques == True):
                             attendance.destroy()
                             
                             
                             
                             #################################### Function for the face Embedding ##############################################################
                    def face_embedding():
                        attendance1.destroy()
                        fe = Toplevel()
                        fe.title("Extract Embeddings")
                        fe.geometry("1400x700+0+0")
                        fe.configure(bg="#202020")
                        
                       
                        embed_title = Label(fe, text="Extract And Save Embeddings", font=("Helvetica", 30, "bold"),
                                            bg="#202020", fg="white")
                        embed_title.place(x=0, y=0, relwidth=1)
                        student_details = embedding_obj.get_student_details()
                        embeddings_model_file = os.path.join(root_dir, "models/embeddings.pickle")
                        if not os.path.exists(embeddings_model_file):
                            [image_ids, image_paths, image_arrays, names, face_ids] = embedding_obj.get_all_face_pixels(
                                student_details)
                            face_pixels = embedding_obj.normalize_pixels(imagearrays=image_arrays)

                            def start_extracting_embedding(pixels):
                                embeddings = []
                                for (i, face_pixel) in enumerate(face_pixels):
                                    j = i + 1
                                    percent.set(str(int((j / l) * 100)) + "%")
                                    text.set(str(j) + "/" + str(l) + "tasks completed")
                                    pgbar["value"] = j
                                    fe.update()
                                    sample = np.expand_dims(face_pixel, axis=0)
                                    embedding = embedding_model.predict(sample)
                                    new_embedding = embedding.reshape(-1)
                                    embeddings.append(new_embedding)
                                data = {"paths": image_paths, "names": names, "face_ids": face_ids,
                                        "imageIDs": image_ids, "embeddings": embeddings}
                                f = open('models/embeddings.pickle', "wb")
                                f.write(pickle.dumps(data))
                                f.close()
                                fe.after(1000, fe.destroy)
                                messagebox.showinfo("Success",
                                                    "Embedding extracted successfully.. New pickle file created to store embeddings",
                                                    parent=attendance)

                            def back():
                                fe.destroy()

                            backbtn = Button(fe, text='Back', fg='White', bg='#FF9900', font=('Helvetica', 18, 'bold'),
                                             command=back).place(x=1250, y=1)
                            l = len(face_pixels)
                            percent = StringVar()
                            text = StringVar()
                            pgbar = Progressbar(fe, length=500, mode='determinate', maximum=l, value=0,
                                                orient=HORIZONTAL)
                            pgbar.place(x=400, y=450)
                            percentlabel = Label(fe, textvariable=percent, font=("Helvetica", 16, "bold"))
                            percentlabel.place(x=475, y=475)
                            textlabel = Label(fe, textvariable=text, font=("Helvetica", 16, "bold"))
                            textlabel.place(x=475, y=500)
                            btn = Button(fe, text="Start Extracting Embeddings", fg='white',
                                         font=("Times new roman", 20, "bold"),
                                         command=lambda: start_extracting_embedding(pixels=face_pixels), bg="#FF9900")
                            btn.place(x=450, y=550)
                            fe.mainloop()

                        else:
                            [old_data, unique_names] = embedding_obj.check_pretrained_file(embeddings_model_file)
                            remaining_names = embedding_obj.get_remaining_names(student_details, unique_names)
                            data = embedding_obj.get_remaining_face_pixels(student_details, remaining_names)
                            if data != None:
                                [image_ids, image_paths, image_arrays, names, face_ids] = data
                                face_pixels = embedding_obj.normalize_pixels(imagearrays=image_arrays)
                                
                                def on_closing ():
                                     fe.destroy()
                                     # Show the main window again
                                     open_admin_panel()
                                
                                fe.protocol("WM_DELETE_WINDOW", on_closing)
                                def start_extracting_embedding(pixels):
                                    embeddings = []
                                    for (i, face_pixel) in enumerate(face_pixels):
                                        j = i + 1
                                        percent.set(str(int((j / l) * 100)) + "%")
                                        text.set(str(j) + "/" + str(l) + "tasks completed")
                                        pgbar["value"] = j
                                        fe.update()
                                        sample = np.expand_dims(face_pixel, axis=0)
                                        embedding = embedding_model.predict(sample)
                                        new_embedding = embedding.reshape(-1)
                                        embeddings.append(new_embedding)
                                    new_data = {"paths": image_paths, "names": names, "face_ids": face_ids,
                                                "imageIDs": image_ids, "embeddings": embeddings}
                                    combined_data = {"paths": [], "names": [], "face_ids": [], "imageIDs": [],
                                                     "embeddings": []}
                                    combined_data["paths"] = old_data["paths"] + new_data["paths"]
                                    combined_data["names"] = old_data["names"] + new_data["names"]
                                    combined_data["face_ids"] = old_data["face_ids"] + new_data["face_ids"]
                                    combined_data["imageIDs"] = old_data["imageIDs"] + new_data["imageIDs"]
                                    combined_data["embeddings"] = old_data["embeddings"] + new_data["embeddings"]

                                    f = open('models/embeddings.pickle', "wb")
                                    f.write(pickle.dumps(combined_data))
                                    f.close()
                                    fe.after(1000, fe.destroy)
                                    messagebox.showinfo("Success",
                                                        "Embedding extracted successfully.. New pickle file created to store embeddings",
                                                        parent=attendance)

                                def back():
                                    fe.destroy()

                                backbtn = Button(fe, text='Back', fg='White', bg='#FF9900',
                                                 font=('Helvetica', 18, 'bold'), command=back).place(x=1250, y=1)
                                l = len(face_pixels)
                                percent = StringVar()
                                text = StringVar()
                                pgbar = Progressbar(fe, length=500, mode='determinate', maximum=l, value=0,
                                                    orient=HORIZONTAL)
                                pgbar.place(x=400, y=450)
                                percentlabel = Label(fe, textvariable=percent, font=("Helvetica", 16, "bold"))
                                percentlabel.place(x=475, y=475)
                                textlabel = Label(fe, textvariable=text, font=("Helvetica", 16, "bold"))
                                textlabel.place(x=475, y=500)
                                btn = Button(fe, text="Start Extracting Embeddings", fg='white',
                                             font=("Helvetica", 20, "bold"),
                                             command=lambda: start_extracting_embedding(pixels=face_pixels),
                                             bg="#FF9900")
                                btn.place(x=450, y=550)
                                fe.mainloop()
                            else:
                                messagebox.showinfo("Warning",
                                                    "No new Student found. Embeddings already existed for these Student")
                                fe.after(1000, fe.destroy)
                    
                        def change():
                            account = Toplevel()
                            account.geometry('500x450+200+200')
                            account.title('Admin Account')
                            account.focus_force()
                            account.grab_set()
                            account_frame = Frame(account, bg='white', height=480, width=500)
                            account_frame.pack()

                            title = Label(account_frame, text="Admin Account", font=('Helvetica', 20, 'bold'),
                                          fg='black',
                                          bg='white', bd=3, relief=SUNKEN)
                            title.place(x=3, y=3, relwidth=1)

                            def back():
                                account.destroy()

                            oldpass_var = StringVar()
                            newuser_var = StringVar()
                            newpass_var = StringVar()
                            backbtn = Button(account, text='Back', bg="#FF9900", fg="black",
                                             font=("Times New Roman", 13, "bold"), borderwidth=1, relief=RIDGE,
                                             command=back).place(x=445, y=7)
                            logo_icon = PhotoImage(file='Photos/logo.png', master=account)
                            admin_logo = Label(account_frame, image=logo_icon, bg='white').place(y=70, relwidth=1)
                            pass_icon = PhotoImage(file='Photos/password.png', master=account)
                            pass_logo = Label(account_frame, image=pass_icon).place(x=7, y=200)
                            pass_label = Label(account_frame, text='Old Password',
                                               font=('times new roman', 14, 'bold')).place(x=55, y=215)
                            pass_entry = Entry(account_frame, show='*', font=('times new roman', 14, 'bold'),
                                               textvariable=oldpass_var).place(x=210, y=215)
                            user_icon = PhotoImage(file='Photos/user.png', master=account)
                            user_logo = Label(account_frame, image=user_icon).place(x=7, y=265)
                            user_label = Label(account_frame, text='New Username',
                                               font=('times new roman', 14, 'bold')).place(x=55, y=275)
                            user_entry = Entry(account_frame, font=('times new roman', 14, 'bold'),
                                               textvariable=newuser_var).place(x=210, y=275)
                            newpass_logo = Label(account_frame, image=pass_icon).place(x=7, y=325)
                            newpass_label = Label(account_frame, text='New Password',
                                                  font=('times new roman', 14, 'bold')).place(x=55, y=335)
                            newpass_entry = Entry(account_frame, show='*', font=('times new roman', 14, 'bold'),
                                                  textvariable=newpass_var).place(x=210, y=325)

                            def user_change():

                                if oldpass_var.get() == "" or newuser_var.get() == "" or newpass_var.get() == "":
                                    messagebox.showerror('Error', ' All fields are Required', parent=account)
                                else:
                                    conn = pymysql.connect(host='localhost', user='root', password='',
                                                           database='recognition')
                                    cur = conn.cursor()
                                    cur.execute('select * from login where password = %s', (oldpass_var.get()))
                                    row = cur.fetchone()
                                    if row == None:

                                        messagebox.showerror('Error', 'Invalid Old Password', parent=account)
                                    else:
                                        cur.execute('update login set password = %s , username = %s',
                                                    (newpass_var.get(), newuser_var.get()))
                                        conn.commit()
                                        conn.close()
                                        messagebox.showinfo('Success', 'Datas Reset Successfully', parent=account)
                                        account.destroy()

                            btn = Button(account_frame, text='Reset', font=('Helvetica', 14, 'bold'), width=10,
                                         bg='#FF9900', command=user_change, relief=GROOVE).place(x=240, y=380)
                            account.mainloop()

                    def face_embedding_for_login():
                        fe = Toplevel()
                        fe.title("Extract Embeddings")
                        fe.geometry("1400x700+0+0")
                        fe.configure(bg="#202020")

                        embed_title = Label(fe, text="Extract And Save Embeddings", font=("Helvetica", 30, "bold"),
                                            bg="#202020", fg="white")
                        embed_title.place(x=0, y=0, relwidth=1)

                        embedding_obj1 = LoginEmbeddingExtractor(model_path='models/facenet_keras.h5')

                        embeddings_model_file = os.path.join(root_dir, "models/login_embeddings.pickle")

                        if not os.path.exists(embeddings_model_file) or embedding_obj1.are_there_new_accounts(
                                embeddings_model_file):
                            login_details = embedding_obj1.get_login_details()
                            login_images = embedding_obj1.get_login_images(login_details)
                            login_face_pixels = embedding_obj1.normalize_pixels(login_images["image_paths"])

                            # Check if login_face_pixels contains any elements
                            if login_face_pixels.any():
                                def start_extracting_embedding(pixels):
                                    embeddings = []
                                    for (i, face_pixel) in enumerate(login_face_pixels):
                                        j = i + 1
                                        percent.set(str(int((j / l) * 100)) + "%")
                                        text.set(str(j) + "/" + str(l) + " tasks completed")
                                        pgbar["value"] = j
                                        fe.update()
                                        sample = np.expand_dims(face_pixel, axis=0)
                                        embedding = embedding_model1.predict(
                                            sample)  # Make sure to define embedding_model
                                        new_embedding = embedding.reshape(-1)
                                        embeddings.append(new_embedding)
                                    data = {"usernames": login_images["usernames"], "embeddings": embeddings}
                                    with open(embeddings_model_file, "wb") as f:
                                        pickle.dump(data, f)
                                    fe.after(1000, fe.destroy)
                                    messagebox.showinfo("Success", "Embeddings extracted and saved successfully.")

                                def back():
                                    fe.destroy()

                                backbtn = Button(fe, text='Back', fg='White', bg='#FF9900',
                                                 font=('Helvetica', 18, 'bold'),
                                                 command=back).place(x=1250, y=1)
                                l = len(login_face_pixels)
                                percent = StringVar()
                                text = StringVar()
                                pgbar = Progressbar(fe, length=500, mode='determinate', maximum=l, value=0,
                                                    orient=HORIZONTAL)
                                pgbar.place(x=400, y=450)
                                percentlabel = Label(fe, textvariable=percent, font=("Helvetica", 16, "bold"))
                                percentlabel.place(x=475, y=475)
                                textlabel = Label(fe, textvariable=text, font=("Helvetica", 16, "bold"))
                                textlabel.place(x=475, y=500)
                                btn = Button(fe, text="Start Extracting Embeddings", fg='white',
                                             font=("Times new roman", 20, "bold"),
                                             command=lambda: start_extracting_embedding(pixels=login_face_pixels),
                                             bg="#FF9900")
                                btn.place(x=450, y=550)
                                fe.mainloop()
                            else:
                                messagebox.showinfo("Info", "No new login images found.")
                        else:
                            messagebox.showinfo("Info",
                                                "Embeddings already exist for login accounts. No new embeddings will be extracted.")

                    def authenticate(username, password):
                        try:
                            conn = pymysql.connect(host='localhost', user='root', password='', database='recognition')
                            cursor = conn.cursor()
                            cursor.execute('SELECT * FROM login WHERE username = %s AND password = %s',
                                           (username, password))
                            row = cursor.fetchone()
                            conn.close()
                            if row is not None:
                                return row[2]  # Return the user_type if authentication successful
                            else:
                                return None  # Return None if authentication fails
                        except pymysql.Error as e:
                            messagebox.showerror('Error', f'Database error: {e}')
                            return None

                    def open_admin_login():
                        username = username_var.get()
                        password = password_var.get()
                        user_type = authenticate(username, password)
                        if user_type is not None and user_type == 'admin':
                            open_admin_panel()
                        else:
                            messagebox.showerror('Error', 'You are not an admin. Please login as admin.')

                    def open_admin_panel():
                        global attendance1
                        attendance1 = Tk()
                        attendance1.title("Facial based Attendance system")
                        attendance1.geometry("1950x900+0+0")

                        # Set background color
                        attendance1.config(bg="#202020")


                        global sideframe
                        sideframe = Frame(attendance1,bg="#202020")
                        sideframe.place(x=270, y=0, width=820, height=900)
                        # Create the login frame
                        sideframe1 = Frame(attendance1, bg="#FF9900")
                        sideframe1.place(x=0, y=0, width= 290, height= 900)


                        ######################################## Face Based Attendance Management Slider ##############################


                        topic = Label(attendance1, text="Admin Acces",bg="#FF9900", fg="white",
                                      font=("Helvetica", 30, "bold"))
                        topic.place(x=10, y=30)

                        B9 = Button(attendance1, text="Add Instructor", font=("Helvetica", 20, "bold"),
                                    fg="White", bg="#FF9900", width=15,
                                    borderwidth=0, highlightthickness=0,command=open_account_creation_form,)

                        B9.place(x=10, y=100)

                        B11 = Button(attendance1, text="Add Student", fg="White", bg="#FF9900",
                                     font=("Helvetica", 20, "bold"),
                                     width=15,borderwidth=0, highlightthickness=0,command=manage_student,)
                        B11.place(x=10, y=180)

                        B12 = Button(attendance1, text="Change Password", font=("Helvetica", 20, "bold"),
                                     fg="White", bg="#FF9900", width=15, borderwidth=0, highlightthickness=0,command=open_change_password_form, )
                        B12.place(x=10, y=260)

                        B13 = Button(attendance1, text="Train Student Data", fg="White", bg="#FF9900",
                                     font=("Helvetica", 20, "bold"),
                                     width=16,borderwidth=0, highlightthickness=0, command=train,)
                        B13.place(x=10, y=420)

                        B14 = Button(attendance1, text="Extract Student Data", fg="White", bg="#FF9900",
                                     font=("Helvetica", 20, "bold"),
                                     width=16, borderwidth=0, highlightthickness=0,command=face_embedding)
                        B14.place(x=10, y=340)

                      

                        B16 = Button(attendance1, text="Extract Instructor Data", fg="White", bg="#FF9900",
                                     font=("Helvetica", 20, "bold"),
                                     width=16, borderwidth=0, highlightthickness=0, command=face_embedding_for_login)
                        B16.place(x=10, y=500)

                        B17 = Button(attendance1, text="Train Instructor Data", fg="White", bg="#FF9900",
                                     font=("Helvetica", 20, "bold"),
                                     width=16, borderwidth=0, highlightthickness=0, command=Logintrain)
                        B17.place(x=10, y=580)
                        # Create a button to open the Excel viewer
                        B15 = Button(attendance1, text="Excel attendance", fg="White", bg="#FF9900",
                                     font=("Helvetica", 20, "bold"),
                                     width=15, borderwidth=0, highlightthickness=0, command=open_excel_viewer)
                        B15.place(x=10, y=660)
                        attendance.mainloop()

                    def open_excel_viewer():
                        try:
                            attendance1.destroy()
                            # Create a new window to display the exported data
                            viewer_window = tk.Toplevel()
                            viewer_window.title("Exported Attendance Reports")
                            
                            def on_closing ():
                                 viewer_window.destroy()
                                 # Show the main window again
                                 open_admin_panel()
                            
                            viewer_window.protocol("WM_DELETE_WINDOW", on_closing)
                            # Function to search files
                            def search_files():
                                query = search_entry.get().strip().lower()
                                searched_files = [f for f in all_exported_files if query in f.lower()]
                                refresh_file_list(searched_files)

                            # Function to sort files by modification time
                            def sort_files_by_date():
                                sorted_files = sorted(all_exported_files,
                                                      key=lambda x: os.path.getmtime(os.path.join(export_folder, x)),
                                                      reverse=True)
                                refresh_file_list(sorted_files)

                            # Function to refresh the file list
                            def refresh_file_list(file_list):
                                for widget in files_frame.winfo_children():
                                    widget.destroy()

                                if not file_list:
                                    label = tk.Label(files_frame, text="No matching files found.",
                                                     font=("Helvetica", 12))
                                    label.pack(pady=20)
                                else:
                                    for file_name in file_list:
                                        def open_file(filename):
                                            os.startfile(os.path.join(export_folder, filename))

                                        # Create a clickable label for each file
                                        label = tk.Label(files_frame, text=file_name, font=("Helvetica", 12), fg="blue",
                                                         cursor="hand2")
                                        label.pack()

                                        # Bind the label to open the file when clicked
                                        label.bind("<Button-1>", lambda event, filename=file_name: open_file(filename))

                            # Create a frame to hold search and sort buttons
                            # Create a frame to hold search and sort buttons with background color
                            button_frame = tk.Frame(viewer_window, bg="#202020")
                            button_frame.pack(side="top", fill="x")

                            # Entry for search query
                            search_entry = tk.Entry(button_frame, font=("Helvetica", 12), bg="#202020", fg="white")
                            search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

                            # Search button
                            search_button = tk.Button(button_frame, text="Sort by Date", font=("Helvetica", 12),
                                                      command=search_files, bg="#FF9900", fg="black")
                            search_button.grid(row=0, column=2, padx=5, pady=10)

                            # Sort button
                            sort_button = tk.Button(button_frame, text="Search", font=("Helvetica", 12),
                                                    command=sort_files_by_date, bg="#FF9900", fg="black")
                            sort_button.grid(row=0, column=1, padx=5, pady=10)

                            # Create a frame to display the list of exported Excel files
                            files_frame = tk.Frame(viewer_window, width=1000, height=600)  # Set width and height
                            files_frame.pack_propagate(0)  # Prevent resizing based on contents
                            files_frame.pack(fill='both', expand=True)
                            files_frame.configure(bg="white")  # Set background color of the main frame

                            # Get a list of all exported Excel files
                            export_folder = 'exports'
                            all_exported_files = [f for f in os.listdir(export_folder) if f.endswith('.xlsx')]

                            # Initially display all files
                            refresh_file_list(all_exported_files)

                        except Exception as e:
                            # Show error message if any error occurs
                            messagebox.showerror("Error", f"An error occurred: {e}")

                    def create_account(username, password, user_type, subject=None):
                        try:
                            # Connect to the database
                            conn = pymysql.connect(host="localhost", user="root", password="", database="recognition")

                            # Create a cursor object to execute queries
                            with conn.cursor() as cursor:
                                # SQL query to insert data into the database
                                if subject:
                                    sql = "INSERT INTO login (username, password, user_type, subject) VALUES (%s, %s, %s, %s)"
                                    cursor.execute(sql, (username, password, user_type, subject))
                                else:
                                    sql = "INSERT INTO login (username, password, user_type) VALUES (%s, %s, %s)"
                                    cursor.execute(sql, (username, password, user_type))

                            # Commit changes to the database
                            conn.commit()

                            # Face capture
                            capture_face_images(username)

                            messagebox.showinfo("Success", "Account created successfully!")
                        except pymysql.Error as e:
                            messagebox.showerror("Error", f"Error creating account: {e}")

                    # Function to capture face images for a user
                    def capture_face_images(username):
                        try:
                            # Create directory if not exists
                            input_directory = os.path.join('dataset_login', username)
                            if not os.path.exists(input_directory):
                                os.makedirs(input_directory, exist_ok=True)

                            # Capture face images
                            count = 1
                            print("[INFO] starting video stream...")
                            video_capture = cv2.VideoCapture(0)
                            while count <= 100:
                                try:
                                    check, frame = video_capture.read()
                                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                                    for (x, y, w, h) in faces:
                                        face = frame[y - 5:y + h + 5, x - 5:x + w + 5]
                                        resized_face = cv2.resize(face, (160, 160))
                                        cv2.imwrite(os.path.join(input_directory, username + str(count) + '.jpg'),
                                                    resized_face)
                                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                                        count += 1

                                    cv2.imshow("Frame", frame)
                                    key = cv2.waitKey(1)
                                    if key == ord('q'):
                                        break
                                except Exception as e:
                                    pass
                            video_capture.release()
                            cv2.destroyAllWindows()

                        except Exception as e:
                            messagebox.showerror("Error", f"Error capturing face images: {e}")

                    def submit_form(username_entry, password_entry, user_type_entry, subject_entry=None):
                        username = username_entry.get()
                        password = password_entry.get()
                        user_type = user_type_entry.get()
                        subject = subject_entry.get() if subject_entry else None

                        if not username or not password or not user_type:
                            messagebox.showerror("Error", "Please fill in all the fields")
                        else:
                            create_account(username, password, user_type, subject)

                    def open_account_creation_form():
                        manage_student_frame1 = Frame(sideframe, bg="#202020")
                        manage_student_frame1.pack(fill=BOTH, expand=True)

                        username_label = Label(manage_student_frame1, text="Username", fg="white", bg="#202020",
                                               font=("Helvetica", 20, "bold"))
                        username_label.place(x=35, y=30)
                        username_entry = Entry(manage_student_frame1, fg="white", bg="#202020",
                                               font=("Helvetica", 20, "bold"))
                        username_entry.place(x=35, y=130)

                        password_label = Label(manage_student_frame1, text="Password:", fg="white", bg="#202020",
                                               font=("Helvetica", 20, "bold"))
                        password_label.place(x=35, y=230)
                        password_entry = Entry(manage_student_frame1, show="*", fg="white", bg="#202020",
                                               font=("Helvetica", 20, "bold"))
                        password_entry.place(x=35, y=330)
                        
                        user_type_label = tk.Label(manage_student_frame1, text="User Type:", fg="white", bg="#202020",
                                                   font=("Helvetica", 20, "bold"))
                        user_type_label.place(x=435, y=30)
                        
                        # Create a ComboBox for user type selection
                        user_type_combobox = ttk.Combobox(manage_student_frame1, values=["Instructor", "Admin"],
                                                          font=("Helvetica", 20, "bold"))
                        user_type_combobox.place(x=435, y=130)
                     

                        subject_label = Label(manage_student_frame1, text="Subject:", fg="white", bg="#202020",
                                              font=("Helvetica", 20, "bold"))
                        subject_label.place(x=435, y=230)

                        subject_entry = Entry(manage_student_frame1, fg="white", bg="#202020",
                                              font=("Helvetica", 20, "bold"))
                        subject_entry.place(x=435, y=330)

                        submit_button = Button(manage_student_frame1, text="Submit", fg="White", bg="#FF9900",
                                               font=("Helvetica", 20, "bold"), width=10,
                                               command=lambda: submit_form(username_entry, password_entry,
                                                                           user_type_combobox, subject_entry))
                        submit_button.place(x=35, y=430)

                        # Call the function to open the account creation form immediately

                    def show_account_creation_form():
                        open_account_creation_form()

                    def change_password(username, current_password, new_password):
                        try:
                            with conn.cursor() as cursor:
                                # Check if the current password is correct
                                cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s",
                                               (username, current_password))
                                user = cursor.fetchone()
                                if user:
                                    # Update the password
                                    cursor.execute("UPDATE login SET password = %s WHERE username = %s",
                                                   (new_password, username))
                                    conn.commit()
                                    messagebox.showinfo("Success", "Password changed successfully!")
                                else:
                                    messagebox.showerror("Error", "Incorrect current password")
                        except pymysql.Error as e:
                            messagebox.showerror("Error", f"Error changing password: {e}")

                    def submit_form1(username_entry, current_password_entry, new_password_entry):
                        username = username_entry.get()
                        current_password = current_password_entry.get()
                        new_password = new_password_entry.get()
                        change_password(username, current_password, new_password)


                    def open_change_password_form():
                        attendance1.destroy()
                        change_password_frame = Tk()
                        change_password_frame.title("Change Password")
                        change_password_frame.geometry("1115x600+0+0")
                        change_password_frame.config(bg="#202020")
                        
                        username_label = Label(change_password_frame, text="Username", fg="white", bg="#202020",
                                           font=("Helvetica", 20, "bold"))
                        username_label.place(x=35, y=30)
                        username_entry = Entry(change_password_frame, fg="white", bg="#202020",
                                           font=("Helvetica", 20, "bold"))
                        username_entry.place(x=35, y=100)

                        current_password_label = Label(change_password_frame, text="Current Password:",fg="white", bg="#202020",
                                           font=("Helvetica", 20, "bold"))
                        current_password_label.place(x=35, y=170)
                        current_password_entry = Entry(change_password_frame, show="*",fg="white", bg="#202020",
                                           font=("Helvetica", 20, "bold"))
                        current_password_entry.place(x=35, y=240)

                        new_password_label = Label(change_password_frame, text="New Password:",fg="white", bg="#202020",
                                           font=("Helvetica", 20, "bold"))
                        new_password_label.place(x=35, y=310)
                        new_password_entry = Entry(change_password_frame, show="*",fg="white", bg="#202020",
                                           font=("Helvetica", 20, "bold"))
                        new_password_entry.place(x=35, y=380)

                        submit_button = Button(change_password_frame, text="Submit",fg="white", bg="#FF9900", width=10,
                                               font=("Helvetica", 20, "bold"),command=lambda: submit_form1(username_entry, current_password_entry,
                                                                           new_password_entry))
                        submit_button.place(x=35, y=450)
                        
                        def on_closing ():
                             change_password_frame.destroy()
                             # Show the main window again
                             open_admin_panel()
                        
                        change_password_frame.protocol("WM_DELETE_WINDOW", on_closing)
                    # Define the function to show the change password form
                    def show_change_password_form():
                        open_change_password_form()

                    def detect_hands():
                        handsvm = cv2.CascadeClassifier('handraising/haarcascade_hand.xml')
                        palmsvm = cv2.CascadeClassifier('handraising/rpalm_cascade.xml')
                        handsvm1 = cv2.CascadeClassifier('handraising/palm_v4.xml')
                        handsvm2 = cv2.CascadeClassifier('handraising/palm.xml')

                        def play_sound():
                            winsound.Beep(500, 300)

                        def detect(gray, frame):
                            hands = handsvm.detectMultiScale(gray, 1.3, 5)
                            palm = palmsvm.detectMultiScale(gray, 1.3, 5)
                            hands1 = handsvm1.detectMultiScale(gray, 1.3, 5)
                            hands2 = handsvm2.detectMultiScale(gray, 1.3, 5)

                            for (x, y, w, h) in hands2:
                                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                                roi_gray = gray[y:y + h, x:x + w]
                                roi_color = frame[y:y + h, x:x + w]

                            for (x, y, w, h) in hands:
                                cv2.putText(frame, 'hand raising', (x, y), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
                                cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 2)

                            for (x, y, w, h) in hands1:
                                cv2.putText(frame, 'hand raising', (x, y), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
                                cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 2)
                                play_sound()

                            for (x, y, w, h) in palm:
                                cv2.putText(frame, 'hand raising', (x, y), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
                                cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 2)
                                play_sound()

                            return frame

                        # Creating a frameless window
                        window = "Frameless Window"
                        cv2.namedWindow(window, cv2.WINDOW_NORMAL)
                        cv2.setWindowProperty(window, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                        cv2.setWindowProperty(window, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_GUI_NORMAL)
                        cv2.moveWindow(window, 400, 130)
                        cv2.resizeWindow(window, 700, 460)

                        # Initializing the camera
                        video_capture = cv2.VideoCapture(1)  # 0 for internal camera, 1 for external camera

                        while True:
                            _, frame = video_capture.read()
                            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                            # Edge detection
                            lower = 115
                            upper = 235
                            canvas = cv2.Canny(gray, lower, upper)

                            # Hand detection
                            detected_frame = detect(gray, frame)

                            # Displaying the detected frames in the frameless window
                            cv2.imshow(window, detected_frame)

                            # Press 'q' to break the loop
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break

                        video_capture.release()
                        cv2.destroyAllWindows()

                    ########################################## Facial Based Attendance system page ##################################

                    attendance = Tk()
                    attendance.title("Facial based Attendance system")
                    attendance.geometry("1950x600+0+0")

                    # Set background color
                    attendance.config(bg="#202020")
                    global sideframe4
                    sideframe4 = Frame(attendance, bg="#202020")
                    sideframe4.place(x=350, y=50, width=820, height=600)
                    ######################################## Face Based Attendance Management Slider ##############################
                    def faceslider():
                        global count, text
                        if (count >= len(manage)):
                            count = -1
                            text = ''
                            topic.config(text=text)
                        else:
                            text = text + manage[count]
                            topic.config(text=text)
                            count += 1
                        topic.after(200, faceslider)

                    manage = username_var.get()
                    topic = Label(attendance, text="Instructor: " + "[" + manage + "]", bg="#202020", fg="white",
                                  font=("Helvetica", 30, "bold"))
                    topic.place(x=20, y=40)

                    B1 = Button(attendance, text="ATTENDANCE REPORT", font=("Helvetica", 20, "bold"),
                                fg="White", bg="#FF9900", width=20, command=report, )
                    B1.place(x=20, y=100)

                    B2 = Button(attendance, text="TIME IN", font=("Helvetica", 20, "bold"),
                                fg="White", bg="#FF9900", width=9, command=time_in, )
                    B2.place(x=20, y=180)

                    B3 = Button(attendance, text="TIME OUT", font=("Helvetica", 20, "bold"),
                                fg="White", bg="#FF9900", width=10, command=time_out, )
                    B3.place(x=190, y=180)


                    B4 = Button(attendance, text="DETECT RAISING", font=("Helvetica", 20, "bold"),
                                 fg="White", bg="#FF9900", width=20, command=detect_hands)
                    B4.place(x=20, y=260)

                    B5 = Button(attendance, text="SEND EMAIL", font=("Helvetica", 20, "bold"),
                                fg="White", bg="#FF9900", width=20, command=trigger_email)
                    B5.place(x=20, y=340)

                    B6 = Button(attendance, text="LOGOUT", font=("Helvetica", 20, "bold"),
                                 fg="White", bg="#FF9900", width=9, command=exit, )
                    B6.place(x=20, y=500)

                    B7 = Button(attendance, text="'Q' TO STOP", font=("Helvetica", 20, "bold"),
                                fg="White", bg="#FF9900", width=10,  )
                    B7.place(x=190, y=500)

                    B8 = Button(attendance, text="Admin Access", fg="White", bg="#FF9900",
                                font=("Helvetica", 20, "bold"),
                                width=20, command=open_admin_login, )
                    B8.place(x=20, y=420)


                    attendance.mainloop()
            except pymysql.err.OperationalError as e:
                messagebox.showerror("Error",
                                     "Sql Connection Error... Open Xamp Control Panel and then start MySql Server ")
            except Exception as e:
                print(e)
                messagebox.showerror("Error", "Close all the windows and restart your program")

count = 0
text = ""


import os
import pickle
import cv2
import numpy as np
from tkinter import messagebox

def face_recognition_login(username):
    recognizer_path = 'models/login_login_recognizer.pickle'
    embeddings_path = 'models/login_embeddings.pickle'
    face_cascade_path = 'models/haarcascade_frontalface_default.xml'

    if not os.path.exists(recognizer_path) or not os.path.exists(embeddings_path):
        messagebox.showerror("Error", "Model not found. Train the model first.")
        return

    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    detection_counter = 0
    if face_cascade.empty():
        messagebox.showerror("Error", "Failed to load face cascade classifier.")
        return

    try:
        embedding_model1 = embedding_obj1.load_model()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load embedding model: {e}")
        return

    try:
        with open(recognizer_path, 'rb') as f:
            recognizer = pickle.load(f)

        with open(embeddings_path, 'rb') as f:
            data = pickle.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load recognizer or embeddings: {e}")
        return

    if 'embeddings' not in data or 'usernames' not in data:
        messagebox.showerror("Error", "Invalid embeddings file. 'embeddings' and 'usernames' keys not found.")
        return

    embeddings = data['embeddings']
    usernames = data['usernames']

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        messagebox.showerror("Error", "Could not open video device.")
        return

    recognized = False
    threshold = 0.7  # Adjusted threshold value for recognition
    scan_counter = 0
    max_scans = 10

    while not recognized:
        try:
            check, frame = video_capture.read()
            if not check:
                print("Failed to capture frame from video stream")
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            if len(faces) > 0:
                for (x, y, w, h) in faces:
                    face = frame[y - 5:y + h + 5, x - 5:x + w + 5]
                    resized_face = cv2.resize(face, (160, 160))

                    processed_face = resized_face.astype("float") / 255.0
                    processed_face = np.expand_dims(processed_face, axis=0)
       
                    preds = liveness_model.predict(processed_face)[0]
                    text = ""

                    if preds > 0.9:  # Spoofing
                        label_name = 'spoof'
                        color = (0, 0, 255)  # Red color for spoofing
                        text = "SPOOF ATTEMPT"
                    elif preds < 0.5:  # Real person
                        label_name = "real"
                        color = (0, 255, 0)  # Green color for real person

                        if label_name == "real":
                            face_pixel = embedding_obj.normalize_pixels(imagearrays=resized_face)
                            sample = np.expand_dims(face_pixel, axis=0)
                            embedding = embedding_model1.predict(sample)
                            embedding = embedding.reshape(1, -1)
                            preds = recognizer.predict_proba(embedding)[0]
                            pred_index = np.argmax(preds)
                            confidence = preds[pred_index]
                            predicted_name = usernames[pred_index]
                            

                            if confidence > threshold:
                                scan_counter += 1
                                if scan_counter >= max_scans:
                                    login_user(predicted_name)
                                    recognized = True
                                    break
                            else:
                                scan_counter = 0  # Reset counter if confidence falls below threshold

                    else:
                        label_name = "none"
                        color = (255, 0, 0)  # Blue color for none

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                cv2.imshow("Frame", frame)

                key = cv2.waitKey(1)
                if key == ord('q'):
                    break

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    video_capture.release()
    cv2.destroyAllWindows()
    
def login_user(username):
    try:
        conn = pymysql.connect(host='localhost', user='root', password='', database='recognition')
        curr = conn.cursor()
        curr.execute('SELECT * FROM login WHERE username = %s', (username,))
        row = curr.fetchone()
        if row is None:
            messagebox.showerror('Error', 'User not found in database.')
        else:
            messagebox.showinfo("Success", f"Welcome {username}!")
            face.destroy()
            
            def manage_student ():
                 try:
                      attendance1.destroy()
                      conn = pymysql.connect(host="localhost", user="root", password="", database="recognition")
                      cur = conn.cursor()
                      first = Toplevel()
                      first.geometry("1350x650")
                      first.config(bg="#FF9900")
                      first.title("Add Student")
                      
                      # Create a frame
                      frame = Frame(first, bg="#FF9900")
                      frame.place(x=0, y=0, width=1350)
                      
                      def on_closing ():
                           first.destroy()
                           # Show the main window again
                           attendance1.deiconify()
                      
                      first.protocol("WM_DELETE_WINDOW", on_closing)
                      
                     
                      # Place the label inside the frame
                      def back ():
                           first.destroy()
                      
                      # All Required variables for database
                      eid_var = StringVar()
                      post_var = StringVar()
                      fname_var = StringVar()
                      gender_var = StringVar()
                      contact_var = StringVar()
                      address_var = StringVar()
                      guardian_name_var = StringVar()
                      guardian_email_var = StringVar()
                      guardian_contact_var = StringVar()
                      dt = datetime.now()
                      DOJ_var = str(dt).split(' ')[0]
                      search_by = StringVar()
                      search_text = StringVar()
                      search_from = StringVar()
                      search_result = StringVar()
                      mydata = []
                      dataset_dir = os.path.join(root_dir, 'dataset')
                      
                      ############################################# Functions of student Management form ##########################################
                      
                      ########################################## To Add the student #####################################
                      def add_student ():
                           conn = pymysql.connect(host="localhost", user="root", password="",
                                                  database="recognition")
                           
                           if post_var.get() == "" or fname_var.get() == "" or gender_var.get() == "" or contact_var.get() == "" or address_var.get() == "":
                                messagebox.showerror("Error", "All fields are Required", parent=first)
                           else:
                                if (re.search('[a-zA-Z]+', fname_var.get())):
                                     if len(contact_var.get()) != 10:
                                          messagebox.showerror('Error', 'Contact Number must be 10 digits',
                                                               parent=first)
                                     else:
                                          if (re.search('^[9]\d{9}$', contact_var.get())):
                                               regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
                                               if (re.search(regex, address_var.get())):
                                                    name = fname_var.get()
                                                    input_directory = os.path.join(dataset_dir, name)
                                                    if not os.path.exists(input_directory):
                                                         os.makedirs(input_directory, exist_ok='True')
                                                         count = 1
                                                         print("[INFO] starting video stream...")
                                                         video_capture = cv2.VideoCapture(1)
                                                         while count <= 100:
                                                              try:
                                                                   check, frame = video_capture.read()
                                                                   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                                                                   faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                                                                   for (x, y, w, h) in faces:
                                                                        face = frame[y - 5:y + h + 5, x - 5:x + w + 5]
                                                                        resized_face = cv2.resize(face, (160, 160))
                                                                        cv2.imwrite(os.path.join(input_directory,
                                                                                                 name + str(
                                                                                                      count) + '.jpg'),
                                                                                    resized_face)
                                                                        cv2.rectangle(frame, (x, y), (x + w, y + h),
                                                                                      (0, 0, 255), 2)
                                                                        count += 1
                                                                   
                                                                   # show the output frame
                                                                   cv2.imshow("Frame", frame)
                                                                   key = cv2.waitKey(1)
                                                                   if key == ord('q'):
                                                                        break
                                                              except Exception as e:
                                                                   pass
                                                         video_capture.release()
                                                         cv2.destroyAllWindows()
                                                         cur1 = conn.cursor()
                                                         cur1.execute(
                                                              "insert into attendance(department,fname,gender,contact_no,email_address,date_of_join,guardian_name,guardian_email,guardian_contact) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                                              (
                                                                   post_var.get(),
                                                                   fname_var.get(),
                                                                   gender_var.get(),
                                                                   contact_var.get(),
                                                                   address_var.get(),
                                                                   DOJ_var,
                                                                   guardian_name_var.get(),
                                                                   guardian_email_var.get(),
                                                                   guardian_contact_var.get()
                                                              ))
                                                         
                                                         conn.commit()
                                                         cur2 = conn.cursor()
                                                         cur2.execute("select eid from attendance where fname=%s ",
                                                                      (name,))
                                                         output = cur2.fetchone()
                                                         (id,) = output
                                                         os.rename(os.path.join(dataset_dir, name),
                                                                   os.path.join(dataset_dir, name + "_" + str(id)))
                                                         display()
                                                         clear()
                                                         conn.close()
                                                         messagebox.showinfo("Success", "All photos are collected",
                                                                             parent=first)
                                                    else:
                                                         if len(os.listdir(input_directory)) == 100:
                                                              messagebox.showwarning("Error",
                                                                                     "Photo already added for this user.. Click Update to update photo",
                                                                                     parent=first)
                                                         else:
                                                              ques = messagebox.askyesnocancel("Notification",
                                                                                               "Directory already exists with incomplete samples. Do you want to delete the directory",
                                                                                               parent=first)
                                                              if (ques == True):
                                                                   shutil.rmtree(input_directory)
                                                                   messagebox.showinfo("Success",
                                                                                       "Directory Deleted..Now you can add the photo samples",
                                                                                       parent=first)
                                               else:
                                                    messagebox.showerror('Error',
                                                                         'Please Enter the Valid Email Address',
                                                                         parent=first)
                                          else:
                                               messagebox.showerror('Error', 'Invalid Phone number', parent=first)
                                else:
                                     messagebox.showerror('Error', 'Full Name must be String Character',
                                                          parent=first)
                      
                      ########################################## To Display the data of student ######################################
                      
                      def display ():
                           conn = pymysql.connect(host="localhost", user="root", password="",
                                                  database="recognition")
                           cur = conn.cursor()
                           cur.execute("select * from attendance")
                           data = cur.fetchall()
                           if len(data) != 0:
                                table1.delete(*table1.get_children())
                                for row in data:
                                     table1.insert('', END, values=row)
                                conn.commit()
                           conn.close()
                      
                      ########################################### To clear the data ###################################################
                      def clear ():
                           eid_var.set("")
                           post_var.set("")
                           fname_var.set("")
                           gender_var.set("")
                           contact_var.set("")
                           address_var.set("")
                           guardian_name_var.set("")
                           guardian_email_var.set("")
                           guardian_contact_var.set("")
                      
                      ##################################### To display the selected items in text field area ##################################
                      def focus_data (event):
                           cursor = table1.focus()
                           contents = table1.item(cursor)
                           row = contents['values']
                           if (len(row) != 0):
                                eid_var.set(row[0])
                                post_var.set(row[1])
                                fname_var.set(row[2])
                                gender_var.set(row[3])
                                contact_var.set(row[4])
                                address_var.set(row[5])
                                guardian_name_var.set(row[6])
                                guardian_email_var.set(row[7])
                                guardian_contact_var.set(row[8])
                      
                      ############################################## To update the data  ################################################
                      def update ():
                           conn = pymysql.connect(host="localhost", user="root", password="",
                                                  database="recognition")
                           cur = conn.cursor()
                           if post_var.get() == "" or fname_var.get() == "" or gender_var.get() == "" or contact_var.get() == "" or address_var.get() == "":
                                messagebox.showerror("Error", "All fields are Required", parent=first)
                           else:
                                if (re.search('[a-zA-Z]+', fname_var.get())):
                                     if len(contact_var.get()) != 10:
                                          messagebox.showerror('Error', 'Contact Number must be 10 digits',
                                                               parent=first)
                                     else:
                                          if (re.search('^[9]\d{9}$', contact_var.get())):
                                               regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
                                               if (re.search(regex, address_var.get())):
                                                    id = eid_var.get()
                                                    name = fname_var.get()
                                                    student_names = os.listdir(dataset_dir)
                                                    student_ids = [x.split('_')[1] for x in student_names]
                                                    if id in student_ids:
                                                         index = student_ids.index(id)
                                                         student_name = student_names[index]
                                                         q = messagebox.askyesno("Notification",
                                                                                 "Do you want to update the photo samples too",
                                                                                 parent=attendance)
                                                         if (q == True):
                                                              input_directory = os.path.join(dataset_dir, student_name)
                                                              shutil.rmtree(input_directory)
                                                              output_directory = os.path.join(dataset_dir,
                                                                                              name + "_" + id)
                                                              os.mkdir(output_directory)
                                                              count = 1
                                                              print("[INFO] starting video stream...")
                                                              video_capture = cv2.VideoCapture(1)
                                                              while count <= 100:
                                                                   try:
                                                                        check, frame = video_capture.read()
                                                                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                                                                        faces = face_cascade.detectMultiScale(gray, 1.3,
                                                                                                              5)
                                                                        for (x, y, w, h) in faces:
                                                                             face = frame[y - 5:y + h + 5,
                                                                                    x - 5:x + w + 5]
                                                                             resized_face = cv2.resize(face, (160, 160))
                                                                             cv2.imwrite(os.path.join(output_directory,
                                                                                                      name + str(
                                                                                                           count) + '.jpg'),
                                                                                         resized_face)
                                                                             cv2.rectangle(frame, (x, y),
                                                                                           (x + w, y + h),
                                                                                           (0, 0, 255), 2)
                                                                             count += 1
                                                                        
                                                                        # show the output frame
                                                                        cv2.imshow("Frame", frame)
                                                                        key = cv2.waitKey(1)
                                                                        if key == ord('q'):
                                                                             break
                                                                   except Exception as e:
                                                                        pass
                                                              video_capture.release()
                                                              cv2.destroyAllWindows()
                                                              cur.execute(
                                                                   "update attendance set department = %s, fname = %s, gender = %s, contact_no = %s, email_address = %s, guardian_name = %s, guardian_email = %s, guardian_contact = %s where eid = %s",
                                                                   (
                                                                        post_var.get(),
                                                                        fname_var.get(),
                                                                        gender_var.get(),
                                                                        contact_var.get(),
                                                                        address_var.get(),
                                                                        guardian_name_var.get(),
                                                                        guardian_email_var.get(),
                                                                        guardian_contact_var.get(),
                                                                        eid_var.get()
                                                                   ))
                                                              conn.commit()
                                                              display()
                                                              clear()
                                                              conn.close()
                                                              messagebox.showinfo("Success",
                                                                                  "Photos and database updated successfully",
                                                                                  parent=first)
                                                         
                                                         else:
                                                              os.rename(os.path.join(dataset_dir, student_name),
                                                                        os.path.join(dataset_dir, name + "_" + id))
                                                              cur.execute(
                                                                   "update attendance set department = %s, fname = %s, gender = %s, contact_no = %s, email_address = %s, guardian_name = %s, guardian_email = %s, guardian_contact = %s where eid = %s",
                                                                   (
                                                                        post_var.get(),
                                                                        fname_var.get(),
                                                                        gender_var.get(),
                                                                        contact_var.get(),
                                                                        address_var.get(),
                                                                        guardian_name_var.get(),
                                                                        guardian_email_var.get(),
                                                                        guardian_contact_var.get(),
                                                                        eid_var.get()
                                                                   ))
                                                              conn.commit()
                                                              display()
                                                              clear()
                                                              conn.close()
                                                              messagebox.showinfo("Success",
                                                                                  "Database updated successfully",
                                                                                  parent=first)
                                                    else:
                                                         ques = messagebox.askyesno("Notification",
                                                                                    "Photo samples for this student did not exist in local directory. Please delete the entry from the database",
                                                                                    parent=attendance)
                                                         if (ques == True):
                                                              delete()
                                                              messagebox.showinfo("Success",
                                                                                  "Database Updated successfully")
                                                         else:
                                                              delete()
                                                              messagebox.showinfo("Success",
                                                                                  "Database Updated successfully")
                                               else:
                                                    messagebox.showerror('Error',
                                                                         'Please Enter the Valid Email Address',
                                                                         parent=first)
                                          else:
                                               messagebox.showerror('Error', 'Invalid Contact number', parent=first)
                                else:
                                     messagebox.showerror('Error', 'Full Name must be String Character',
                                                          parent=first)
                      
                      ################################################# To delete the items ###################################################
                      def delete ():
                           conn = pymysql.connect(host="localhost", user="root", password="",
                                                  database="recognition")
                           cur = conn.cursor()
                           if post_var.get() == "" or fname_var.get() == "" or gender_var.get() == "" or contact_var.get() == "" or address_var.get() == "":
                                messagebox.showerror("Error", "All fields are Required", parent=first)
                           else:
                                try:
                                     input_name = fname_var.get() + "_" + eid_var.get()
                                     student_input = os.path.join(dataset_dir, input_name)
                                     if not os.path.exists(student_input):
                                          cur.execute("delete from attendance where eid = %s", eid_var.get())
                                     else:
                                          cur.execute("delete from attendance where eid = %s", eid_var.get())
                                          shutil.rmtree(student_input)
                                     conn.commit()
                                     conn.close()
                                     display()
                                     clear()
                                except Exception as e:
                                     messagebox.showerror("Error", e)
                      
                      def search_data ():
                           conn = pymysql.connect(host="localhost", user="root", password="",
                                                  database="recognition")
                           cur = conn.cursor()
                           cur.execute(
                                "select * from attendance where " + str(search_from.get()) + " LIKE '%" + str(
                                     search_result.get()) + "%'")
                           data = cur.fetchall()
                           if len(data) != 0:
                                table1.delete(*table1.get_children())
                                for row in data:
                                     table1.insert('', END, values=row)
                                conn.commit()
                           else:
                                messagebox.showinfo('Sorry', 'No Data Found', parent=first)
                           conn.close()
                      
                      def show_data ():
                           display()
                           
                           ################################################## student Management form ###################################
                      
                      f2 = Frame(first, bg="#202020", borderwidth="3", relief=SUNKEN, height=740, width=420)
                      titles = Label(f2, text="Add Student", fg="white", bg="#202020",
                                     font=("Helvetica", 20, "bold")).place(x=90, y=30)
                      id = Label(f2, text="Student ID", fg="white", bg="#202020",
                                 font=("Helvetica", 13, "bold")).place(x=35, y=100)
                      E1 = Entry(f2, state="disabled", width=20, textvariable=eid_var,
                                 font=("italic", 13, "bold")).place(x=35, y=130)
                      post = Label(f2, text="Year", fg="white", bg="#202020",
                                   font=("Helvetica", 13, "bold")).place(x=35, y=160)
                      E2 = Entry(f2, width=20, textvariable=post_var, font=("italic", 13, "bold")).place(x=35,
                                                                                                         y=190)
                      name = Label(f2, text="Full Name", fg="white", bg="#202020",
                                   font=("Helvetica", 13, "bold")).place(x=35, y=220)
                      E3 = Entry(f2, width=20, textvariable=fname_var, font=("italic", 12, "bold")).place(x=35,
                                                                                                          y=250)
                      gender = Label(f2, text="Gender", fg="white", bg="#202020",
                                     font=("Helvetica", 12, "bold")).place(x=35, y=280)
                      E7 = Combobox(f2, textvariable=gender_var, values=["Male", "Female", "Others"],
                                    state="readonly", font=("italic", 11, "bold")).place(x=35, y=310)
                      no = Label(f2, text="Contact.No", fg="white", bg="#202020",
                                 font=("Helvetica", 12, "bold")).place(x=35, y=340)
                      E4 = Entry(f2, width=20, textvariable=contact_var, font=("Helvetica", 12, "bold")).place(
                           x=35, y=370)
                      address = Label(f2, text=" Email Address", fg="white", bg="#202020",
                                      font=("Helvetica", 12, "bold")).place(x=35, y=400)
                      E5 = Entry(f2, width=20, textvariable=address_var, font=("italic", 12, "bold")).place(x=35,
                                                                                                            y=430)
                      # Guardian Information
                      guardian_name_label = Label(f2, text="Guardian Name", fg="white", bg="#202020",
                                                  font=("Helvetica", 12, "bold")).place(x=35, y=460)
                      E6 = Entry(f2, width=20, textvariable=guardian_name_var, font=("italic", 12, "bold")).place(
                           x=35,
                           y=490)
                      guardian_email_label = Label(f2, text="Guardian Email", fg="white", bg="#202020",
                                                   font=("Helvetica", 12, "bold")).place(x=35, y=520)
                      E8 = Entry(f2, width=20, textvariable=guardian_email_var,
                                 font=("italic", 12, "bold")).place(x=35,
                                                                    y=550)
                      guardian_contact_label = Label(f2, text="Guardian Contact", fg="white", bg="#202020",
                                                     font=("Helvetica", 12, "bold")).place(x=35, y=580)
                      E9 = Entry(f2, width=20, textvariable=guardian_contact_var,
                                 font=("italic", 12, "bold")).place(x=35,
                                                                    y=610)
                      
                      f2.place(x=10, y=20)
                      # b2 = Button(first, text = "Close", command = first.destroy ).place(x = 135, y = 600)
                      f3 = Frame(first, bg="#202020", height=60, width=402)
                      btn1 = Button(f3, text="Add", bg="#FF9900", height="1", width="7", command=add_student,
                                    font=("Helvetica", 14, "bold")).place(x=5, y=10)
                      btn2 = Button(f3, text="Update", bg="#FF9900", height="1", width="7", command=update,
                                    font=("Helvetica", 14, "bold")).place(x=105, y=10)
                      btn3 = Button(f3, text="Delete", bg="#FF9900", height="1", width="7", command=delete,
                                    font=("Helvetica", 14, "bold")).place(x=205, y=10)
                      btn4 = Button(f3, text="Clear", bg="#FF9900", height="1", width="7", command=clear,
                                    font=("Helvetica", 14, "bold")).place(x=305, y=10)
                      # btn5 = Button(f3, text = "Add Photo Sample", bg = "yellow", height = "2", width = "34",command = add_photo, font = ("Times new Roman", 14 , "bold")).place(x = 10, y = 60)
                      f3.place(x=20, y=690)
                      
                      ########################################## Large Frame ###########################################################
                      f4 = Frame(first, height=740, width=1090, bg="#202020", borderwidth="3", relief=SUNKEN)
                      f4.place(x=440, y=18)
                      l1 = Label(first, text="Search By:", font=("Helvetica", 18, "bold"), bg="#202020",
                                 fg="white").place(x=460, y=25)
                      c1 = Combobox(first, textvariable=search_from, values=["eid", "fname", "post"],
                                    state="readonly", width="25").place(x=600, y=29)
                      E7 = Entry(first, textvariable=search_result, width="25", font=("Helvetica", 10)).place(
                           x=800, y=29)
                      btn7 = Button(first, text="Search ", height="1", width="12", command=search_data,
                                    font=("Helvetica", 13, "bold")).place(x=990, y=25)
                      btn8 = Button(first, text="Show All", height="1", width="12", command=show_data,
                                    font=("Helvetica", 13, "bold")).place(x=1180, y=25)
                      
                      ########################################## Table frame ###########################################################
                      f5 = Frame(f4, bg="#202020", borderwidth="2", relief=SUNKEN)
                      f5.place(x=20, y=45, height=670, width=1050)
                      scroll_x = Scrollbar(f5, orient=HORIZONTAL)
                      scroll_y = Scrollbar(f5, orient=VERTICAL)
                      table1 = Treeview(f5, columns=(
                           "eid", "post", "fname", "gender", "contact.no", "address", "guardian_name",
                           "guardian_email", "guardian_contact", "DOJ"),
                                        xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
                      scroll_x.pack(side=BOTTOM, fill=X)
                      scroll_y.pack(side=RIGHT, fill=Y)
                      scroll_x.config(command=table1.xview)
                      scroll_y.config(command=table1.yview)
                      table1.heading("eid", text="Student ID")
                      table1.heading('post', text="Year")
                      table1.heading("fname", text="Full Name")
                      table1.heading("gender", text="Gender")
                      table1.heading("contact.no", text="Contact_No")
                      table1.heading("address", text=" Email Address")
                      table1.heading("guardian_name", text="Guardian Name")
                      table1.heading("guardian_email", text="Guardian Email")
                      table1.heading("guardian_contact", text="Guardian Contact")
                      table1.heading("DOJ", text="Date Of Join")
                      
                      table1['show'] = 'headings'
                      table1.column("eid", width=100)
                      table1.column("post", width=100)
                      table1.column("fname", width=100)
                      table1.column("gender", width=100)
                      table1.column("contact.no", width=100)
                      table1.column("address", width=100)
                      table1.column("guardian_name", width=100)
                      table1.column("guardian_email", width=100)
                      table1.column("guardian_contact", width=100)
                      table1.column("DOJ", width=100)
                      table1.pack(fill=BOTH, expand=1)
                      table1.bind("<ButtonRelease-1>", focus_data)
                      display()
                      first.mainloop()
                 except pymysql.err.OperationalError as e:
                      messagebox.showerror("Error",
                                           "Sql Connection Error... Open Xamp Control Panel and then start MySql Server ")
                 except Exception as e:
                      print(e)
                      messagebox.showerror("Error", "Close all the windows and restart your program")
            
            def train ():
                 try:
                      attendance1.destroy()
                      second = Toplevel()
                      second.title("Train The System")
                      second.geometry("1400x700+0+0")
                      second.configure(bg="#202020")
                      
                      train_title = Label(second, text="Train the System", fg='white',
                                          font=("Helvetica", 20, "bold"), bg="#202020")
                      train_title.place(x=0, y=0, relwidth=1)
                      
                      def on_closing ():
                           second.destroy()
                           # Show the main window again
                           open_admin_panel()
                      
                      second.protocol("WM_DELETE_WINDOW", on_closing)
                      def back ():
                           second.destroy()
                      
                      backbtn = Button(second, text='Back', fg='black', bg='white', font=('Helvetica', 15),
                                       height=1, width=7, command=back)
                      backbtn.place(x=1260, y=3)
                      
                     
                      def progress ():
                           progress_bar.start(5)
                           try:
                                training_obj = Training(embedding_path='models/embeddings.pickle')
                                label_encoder, labels, embeddings, ids = training_obj.load_embeddings_and_labels()
                                
                                print("Length of ids:", len(ids))
                                print("Length of labels:", len(labels))
                                print("Length of embeddings:", len(embeddings))
                                
                                # Ensure that each label has a corresponding embedding
                                unique_labels = set(labels)
                                filtered_labels = []
                                filtered_embeddings = []
                                for label in unique_labels:
                                     indices = [i for i, l in enumerate(labels) if l == label]
                                     filtered_labels.extend([label] * len(indices))
                                     filtered_embeddings.extend([embeddings[i] for i in indices])
                                
                                # Convert filtered labels to numpy array
                                filtered_labels = np.array(filtered_labels)
                                
                                recognizer = training_obj.create_svm_model(filtered_labels, filtered_embeddings)
                                with open('models/recognizer.pickle', "wb") as f1:
                                     pickle.dump(recognizer, f1)
                                
                                messagebox.showinfo("Success",
                                                    "Training Done Successfully. New pickle file created to store Face Recognition Model",
                                                    parent=second)
                                second.after(1000, second.destroy)
                           except FileNotFoundError as e:
                                second.after(1000, second.destroy)
                                messagebox.showerror("Error",
                                                     f"Pickle file for embeddings is missing. {str(e).split(':')[-1]} not found. First Extract Embeddings and then try again")
                           except ValueError as e:
                                second.after(1000, second.destroy)
                                messagebox.showerror("Error", str(e))
                           except Exception as e:
                                second.after(1000, second.destroy)
                                messagebox.showerror("Error", f"{e} not found.")
                      
                      progress_bar = Progressbar(second, orient=HORIZONTAL, length=500, mode='determinate')
                      progress_bar.place(x=430, y=520)
                      btn = Button(second, text="Start Training", fg='white', font=("Helvetica", 20, "bold"),
                                   command=progress, bg="#FF9900")
                      btn.place(x=600, y=450)
                      second.mainloop()
                 except Exception as e:
                      second.after(1000, second.destroy)
                      messagebox.showerror("Error", "{} not found.".format(e))
            
            def Logintrain ():
                 try:
                      second = Toplevel()
                      second.title("Train The System")
                      second.geometry("1400x700+0+0")
                      second.configure(bg="#202020")
                      train_title = Label(second, text="Train the System", fg='white',
                                          font=("Helvetica", 20, "bold"), bg="#202020")
                      train_title.place(x=0, y=0, relwidth=1)
                      
                      def back ():
                           second.destroy()
                      
                      backbtn = Button(second, text='Back', fg='black', bg='white', font=('Helvetica', 15),
                                       height=1, width=7, command=back)
                      backbtn.place(x=1260, y=3)
                      
                      def progress ():
                           progress_bar.start(5)
                           try:
                                embedding_path = os.path.join('models', 'login_embeddings.pickle')
                                
                                # Training for face login recognizer
                                face_login_training_obj = LoginTraining(embedding_path=embedding_path,
                                                                        recognizer_type='login')
                                [label, labels, Embeddings,
                                 usernames] = face_login_training_obj.load_embeddings_and_labels()
                                face_login_recognizer = face_login_training_obj.create_svm_model(labels=labels,
                                                                                                 embeddings=Embeddings)
                                face_login_training_obj.save_recognizer(face_login_recognizer)
                                
                                # Training for face attendance recognizer
                                
                                messagebox.showinfo("Success",
                                                    "Training Done Successfully. New pickle files created to store Face Login and Face Attendance Recognizers",
                                                    parent=second)
                                second.after(1000, second.destroy)
                           except FileNotFoundError as e:
                                second.after(1000, second.destroy)
                                messagebox.showerror("Error",
                                                     f"Pickle file for embeddings is missing. {str(e).split(':')[-1]} not found. First Extract Embeddings and then try again")
                           except ValueError as e:
                                second.after(1000, second.destroy)
                                messagebox.showerror("Error", str(e))
                           except Exception as e:
                                second.after(1000, second.destroy)
                                messagebox.showerror("Error", f"{e} not found.")
                      
                      progress_bar = Progressbar(second, orient='horizontal', length=500, mode='determinate')
                      progress_bar.place(x=430, y=520)
                      btn = Button(second, text="Start Training", fg='white', font=("Helvetica", 20, "bold"),
                                   command=progress, bg="#FF9900")
                      btn.place(x=600, y=450)
                      second.mainloop()
                 except Exception as e:
                      second.after(1000, second.destroy)
                      messagebox.showerror("Error", f"{e} not found.")
                 
                 ######################################## email automation ######################
            
            def excel():
                 try:
                      conn = pymysql.connect(host="localhost", user="root", password="",
                                             database="recognition")
                      cur = conn.cursor()
                      
                      # Fetch username and subject from the login table based on the logged-in username
                      cur.execute("SELECT username, subject FROM login WHERE username = %s",
                                  (logged_in_username,))
                      user_info = cur.fetchone()
                      if user_info:
                           username, subject = user_info
                      else:
                           username = "N/A"
                           subject = "N/A"
                      
                      # Fetch data from the report table
                      cur.execute("SELECT * FROM report")
                      data = cur.fetchall()
                      
                      print("Fetched data:", data)  # Print fetched data for debugging
                      
                      if len(data) != 0:
                           df = pd.DataFrame(data,
                                             columns=['ID', 'Year', 'Name', 'Date', 'Time', 'Status',
                                                      'Subject'])
                           
                           print("DataFrame created successfully.")  # Print message for debugging
                           
                           now = datetime.now()
                           current_date_time = now.strftime("%Y_%m_%d_%H_%M")
                           
                           folder = 'exports'
                           if not os.path.exists(folder):
                                os.makedirs(folder)
                           
                           excel_filename = os.path.join(folder,
                                                         f'attendance_report_Instructor_{logged_in_username}_Subject_{subject}_Date_created_{current_date_time}.xlsx')
                           
                           print("Excel filename:", excel_filename)  # Print filename for debugging
                           
                           df.to_excel(excel_filename, index=False)
                           
                           print("Excel file created successfully.")  # Print message for debugging
                           
                           messagebox.showinfo("Success",
                                               f"Data has been exported to {excel_filename} successfully. Username: {username}, Subject: {subject}")
                      else:
                           messagebox.showinfo("Information", "No data found to export.")
                      
                      conn.close()
                 except Exception as e:
                      messagebox.showerror("Error", f"An error occurred: {e}")
                      
            def trigger_email ():
                 try:
                      send_mail()  # Call the send_mail function
                      messagebox.showinfo("Success",
                                          "Emails sent successfully!")  # Display a success message
                 except Exception as e:
                      messagebox.showerror("Error", f"An error occurred: {str(e)}")
                 
                 ######################################### Function to recognize the face #######################################
            
            def distance (emb1, emb2):
                 return np.sqrt(np.square(emb1 - emb2))
            
            def getkey (val, student_details):
                 for key, value in student_details.items():
                      if val == value:
                           return key
                 return "Unknown"
            
            def time_in ():
                 start_time = datetime.now()
                 embeddings_model_file = os.path.join(root_dir, "models/embeddings.pickle")
                 recognizer_model_file = os.path.join(root_dir, "models/recognizer.pickle")
                 predictions = []
                 spoof_attempts = []
                 liveness_predictor = []
                 detection_counter = 0  # Counter to track the number of detections
                 # Check if model files exist
                 if os.path.exists(embeddings_model_file) and os.path.exists(recognizer_model_file):
                      try:
                           # Load embeddings and labels
                           training_obj = Training(embedding_path='models/embeddings.pickle')
                           [label, labels, Embeddings, ids] = training_obj.load_embeddings_and_labels()
                           student_details = embedding_obj.get_student_details()
                           # Load recognizer model
                           recognizer = pickle.loads(open('models/recognizer.pickle', "rb").read())
                           # Start video stream
                           vs = cv2.VideoCapture(1)
                           print("[INFO] starting video stream...")
                           window_name = "Frameless Window"
                           cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                           # Set window flags to remove the title bar
                           cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                           cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_GUI_NORMAL)
                           # Set the initial position
                           cv2.moveWindow(window_name, 400, 130)
                           # Set fixed size
                           cv2.resizeWindow(window_name, 700, 460)
                      except Exception as e:
                           # Display error message
                           messagebox.showerror("Error", e)
                           return
                      
                      # Main loop for face recognition
                      while True:
                           try:
                                # Capture frame from video stream
                                (ret, frame) = vs.read()
                                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                                # Detect faces in the frame
                                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                                # Loop through detected faces
                                for (x, y, w, h) in faces:
                                     # Extract face region
                                     face = frame[y - 5:y + h + 5, x - 5:x + w + 5]
                                     resized_face = cv2.resize(face, (160, 160))
                                     # Preprocess face for prediction
                                     processed_face = resized_face.astype("float") / 255.0
                                     processed_face = img_to_array(processed_face)
                                     processed_face = np.expand_dims(processed_face, axis=0)
                                     # Predict liveness of the face
                                     preds = liveness_model.predict(processed_face)[0]
                                     text = "UNKNOWN"
                                     # Determine label color based on liveness prediction
                                     if preds > 0.9:  # Spoofing
                                          label_name = 'spoof'
                                          color = (0, 0, 255)  # Red color for spoofing
                                          spoof_attempts.append((x, y, w, h))  # Record spoof attempts
                                          text = "SPOOF ATTEMPT"
                                     elif preds < 0.5:  # Real person
                                          label_name = "real"
                                          color = (0, 255, 0)  # Green color for real person
                                          detection_counter += 1  # Increment the detection counter
                                          if label_name == "real":  # Check if it's a real person
                                               # Normalize pixels and predict embedding
                                               face_pixel = embedding_obj.normalize_pixels(
                                                    imagearrays=resized_face)
                                               sample = np.expand_dims(face_pixel, axis=0)
                                               embedding = embedding_model.predict(sample)
                                               embedding = embedding.reshape(1, -1)
                                               # Recognize face using the recognizer model
                                               preds = recognizer.predict_proba(embedding)[0]
                                               p = np.argmax(preds)
                                               proba = preds[p]
                                               if proba > 0.8:  # Confidence threshold for recognition
                                                    id = label.classes_[p]
                                                    name = getkey(id, student_details)
                                                    # Fetch department data from the database
                                                    cur = conn.cursor()
                                                    cur.execute("SELECT department FROM attendance WHERE eid = %s",
                                                                (id,))
                                                    department_result = cur.fetchone()
                                                    department = department_result[
                                                         0] if department_result else "Unknown"
                                                    text = "{} {} - {}".format(name, id, department)
                                                    predictions.append(id)
                                          else:
                                               text = "UNKNOWN"
                                               color = (255, 0, 0)
                                               # Display "UNKNOWN" for unrecognized real persons
                                     else:  # None
                                          label_name = "none"
                                          color = (255, 0, 0)  # Blue color for none
                                          if label_name != "spoof":  # Only set text to "UNKNOWN" if it's not a spoof attempt
                                               text = "UNKNOWN"
                                     # Update liveness predictor list
                                     liveness_predictor.append(label_name)
                                     # Determine text to display on frame
                                     if label_name != "spoof":
                                          if label_name == "real":
                                               # Normalize pixels and predict embedding
                                               face_pixel = embedding_obj.normalize_pixels(
                                                    imagearrays=resized_face)
                                               sample = np.expand_dims(face_pixel, axis=0)
                                               embedding = embedding_model.predict(sample)
                                               embedding = embedding.reshape(1, -1)
                                               # Recognize face using the recognizer model
                                               preds = recognizer.predict_proba(embedding)[0]
                                               p = np.argmax(preds)
                                               proba = preds[p]
                                               if proba > 0.8:  # Confidence threshold for recognition
                                                    id = label.classes_[p]
                                                    name = getkey(id, student_details)
                                                    # Fetch department data from the database
                                                    cur = conn.cursor()
                                                    cur.execute("SELECT department FROM attendance WHERE eid = %s",
                                                                (id,))
                                                    department_result = cur.fetchone()
                                                    department = department_result[
                                                         0] if department_result else "Unknown"
                                                    text = "{} {} - {}".format(name, id, department)
                                                    predictions.append(id)
                                     # Draw rectangle and put text on the frame
                                     cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                                     cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color,
                                                 2)
                                # Display frame in OpenCV window
                                cv2.imshow(window_name, frame)
                                key = cv2.waitKey(1) & 0xFF
                                if key == ord('q'):
                                     break
                           except Exception as e:
                                # Display error message
                                messagebox.showerror("Error", e)
                                break
                      # Release video stream and close OpenCV windows
                      vs.release()
                      cv2.destroyAllWindows()
                      
                      # Remaining code for attendance recording...
                      # Remaining code for attendance recording...
                      all_student_ids = set(student_details.values())
                      # Find out which students didn't scan
                      students_absent = all_student_ids - set(predictions)
                      
                      if detection_counter >= 10:
                           # Record attendance for the detected real person
                           for final_id in set(predictions):
                                final_name = getkey(final_id, student_details)
                                print(final_name)
                                print(final_id)
                                
                                late_threshold = 600
                                absent_threshold = 900
                                
                                time_difference = (datetime.now() - start_time).total_seconds()
                                print("Time Difference:", time_difference)
                                
                                if time_difference <= late_threshold:
                                     status = "Present"
                                elif late_threshold < time_difference <= absent_threshold:
                                     status = "Late"
                                else:
                                     status = "Absent"
                                
                                print("Late Threshold:", late_threshold)
                                print("Absent Threshold:", absent_threshold)
                                print("Status:", status)
                                
                                # Show info messagebox for attendance status
                                messagebox.showinfo("Attendance Status",
                                                    "Hello {}. Your attendance is recorded as {}.".format(
                                                         final_name, status))
                                
                                # Fetch department data from the database
                                cur = conn.cursor()
                                cur.execute("SELECT department FROM attendance WHERE eid = %s", (final_id,))
                                department_result = cur.fetchone()
                                department = department_result[0] if department_result else "Unknown"
                                
                                # Fetch subject data for the logged-in user
                                cur.execute("SELECT subject FROM login WHERE username = %s", (logged_in_username,))
                                subject_result = cur.fetchone()
                                subject = subject_result[0] if subject_result else "Unknown"
                                
                                # Insert attendance record into report
                                cur2 = conn.cursor()
                                cur2.execute(
                                     "INSERT INTO report(id, name, department, subject, date, time, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                     (final_id, final_name, department, subject, date.today(),
                                      datetime.now().strftime("%H:%M:%S"),
                                      status))
                                conn.commit()
                      
                      # Handle students who didn't scan but should be marked as absent
                      for absent_id in students_absent:
                           absent_name = getkey(absent_id, student_details)
                           print(absent_name)
                           print(absent_id)
                           
                           absent_threshold = 1
                           
                           time_difference = (datetime.now() - start_time).total_seconds()
                           print("Time Difference:", time_difference)
                           
                           if time_difference > absent_threshold:
                                status = "Absent"
                                
                                # Fetch department data from the database
                                cur = conn.cursor()
                                cur.execute("SELECT department FROM attendance WHERE eid = %s", (absent_id,))
                                department_result = cur.fetchone()
                                department = department_result[0] if department_result else "Unknown"
                                
                                # Fetch subject data for the logged-in user
                                cur.execute("SELECT subject FROM login WHERE username = %s", (logged_in_username,))
                                subject_result = cur.fetchone()
                                subject = subject_result[0] if subject_result else "Unknown"
                                
                                # Insert attendance record into report
                                cur2 = conn.cursor()
                                cur2.execute(
                                     "INSERT INTO report(id, name, department, subject, date, time, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                     (absent_id, absent_name, department, subject, date.today(),
                                      datetime.now().strftime("%H:%M:%S"),
                                      status))
                                conn.commit()
                                
                                # Show info messagebox for attendance status
                                messagebox.showinfo("Attendance Status",
                                                    "Hello {}. Your attendance is recorded as {}.".format(
                                                         absent_name, status))
                      
                      # Display spoof attempts
                      if spoof_attempts:
                           messagebox.showinfo("Spoof Attempts Detected",
                                               "Spoof attempts detected. No attendance recorded for these attempts.")
                           
                           cv2.destroyAllWindows()
                      
                      else:
                           messagebox.showinfo("No Spoof Attempts Detected", "No spoof attempts detected")
                 
                 else:
                      messagebox.showerror("Error",
                                           "Model files not found. Embeddings.pickle file and Recognizer.pickle file must exist within models directory.")
            
            def time_out ():
                 start_time = datetime.now()
                 embeddings_model_file = os.path.join(root_dir, "models/embeddings.pickle")
                 recognizer_model_file = os.path.join(root_dir, "models/recognizer.pickle")
                 predictions = []
                 spoof_attempts = []
                 liveness_predictor = []
                 detection_counter = 0  # Counter to track the number of detections
                 
                 # Check if model files exist
                 if os.path.exists(embeddings_model_file) and os.path.exists(recognizer_model_file):
                      try:
                           # Load embeddings and labels
                           training_obj = Training(embedding_path='models/embeddings.pickle')
                           [label, labels, Embeddings, ids] = training_obj.load_embeddings_and_labels()
                           student_details = embedding_obj.get_student_details()
                           
                           # Load recognizer model
                           recognizer = pickle.loads(open('models/recognizer.pickle', "rb").read())
                           
                           # Start video stream
                           vs = cv2.VideoCapture(1)
                           print("[INFO] starting video stream...")
                           window_name = "Frameless Window"
                           cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                           
                           # Set window flags to remove the title bar
                           cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                           cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_GUI_NORMAL)
                           
                           # Set the initial position
                           cv2.moveWindow(window_name, 400, 130)
                           
                           # Set fixed size
                           cv2.resizeWindow(window_name, 700, 460)
                      except Exception as e:
                           # Display error message
                           messagebox.showerror("Error", e)
                           return
                      
                      # Main loop for face recognition
                      while True:
                           try:
                                # Capture frame from video stream
                                (ret, frame) = vs.read()
                                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                                
                                # Detect faces in the frame
                                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                                
                                # Loop through detected faces
                                for (x, y, w, h) in faces:
                                     # Extract face region
                                     face = frame[y - 5:y + h + 5, x - 5:x + w + 5]
                                     resized_face = cv2.resize(face, (160, 160))
                                     
                                     # Preprocess face for prediction
                                     processed_face = resized_face.astype("float") / 255.0
                                     processed_face = img_to_array(processed_face)
                                     processed_face = np.expand_dims(processed_face, axis=0)
                                     
                                     # Predict liveness of the face
                                     preds = liveness_model.predict(processed_face)[0]
                                     text = "UNKNOWN"
                                     # Determine label color based on liveness prediction
                                     if preds > 0.9:  # Spoofing
                                          label_name = 'spoof'
                                          color = (0, 0, 255)  # Red color for spoofing
                                          spoof_attempts.append((x, y, w, h))  # Record spoof attempts
                                          text = "SPOOF ATTEMPT"
                                     elif preds < 0.5:  # Real person
                                          label_name = "real"
                                          color = (0, 255, 0)  # Green color for real person
                                          detection_counter += 1  # Increment the detection counter
                                          if label_name == "real":  # Check if it's a real person
                                               # Normalize pixels and predict embedding
                                               face_pixel = embedding_obj.normalize_pixels(
                                                    imagearrays=resized_face)
                                               sample = np.expand_dims(face_pixel, axis=0)
                                               embedding = embedding_model.predict(sample)
                                               embedding = embedding.reshape(1, -1)
                                               
                                               # Recognize face using the recognizer model
                                               preds = recognizer.predict_proba(embedding)[0]
                                               p = np.argmax(preds)
                                               proba = preds[p]
                                               if proba > 0.8:  # Confidence threshold for recognition
                                                    id = label.classes_[p]
                                                    name = getkey(id, student_details)
                                                    
                                                    # Fetch department data from the database
                                                    cur = conn.cursor()
                                                    cur.execute("SELECT department FROM attendance WHERE eid = %s",
                                                                (id,))
                                                    department_result = cur.fetchone()
                                                    department = department_result[
                                                         0] if department_result else "Unknown"
                                                    
                                                    text = "{} {} - {}".format(name, id, department)
                                                    predictions.append(id)
                                          else:
                                               text = "UNKNOWN"
                                               color = (255, 0, 0)
                                               # Display "UNKNOWN" for unrecognized real persons
                                     else:  # None
                                          label_name = "none"
                                          color = (255, 0, 0)  # Blue color for none
                                          if label_name != "spoof":  # Only set text to "UNKNOWN" if it's not a spoof attempt
                                               text = "UNKNOWN"
                                     
                                     # Update liveness predictor list
                                     liveness_predictor.append(label_name)
                                     
                                     # Determine text to display on frame
                                     if label_name != "spoof":
                                          if label_name == "real":
                                               # Normalize pixels and predict embedding
                                               face_pixel = embedding_obj.normalize_pixels(
                                                    imagearrays=resized_face)
                                               sample = np.expand_dims(face_pixel, axis=0)
                                               embedding = embedding_model.predict(sample)
                                               embedding = embedding.reshape(1, -1)
                                               
                                               # Recognize face using the recognizer model
                                               preds = recognizer.predict_proba(embedding)[0]
                                               p = np.argmax(preds)
                                               proba = preds[p]
                                               if proba > 0.8:  # Confidence threshold for recognition
                                                    id = label.classes_[p]
                                                    name = getkey(id, student_details)
                                                    
                                                    # Fetch department data from the database
                                                    cur = conn.cursor()
                                                    cur.execute("SELECT department FROM attendance WHERE eid = %s",
                                                                (id,))
                                                    department_result = cur.fetchone()
                                                    department = department_result[
                                                         0] if department_result else "Unknown"
                                                    
                                                    text = "{} {} - {}".format(name, id, department)
                                                    predictions.append(id)
                                     
                                     # Draw rectangle and put text on the frame
                                     cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                                     cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color,
                                                 2)
                                
                                # Display frame in OpenCV window
                                cv2.imshow(window_name, frame)
                                key = cv2.waitKey(1) & 0xFF
                                if key == ord('q'):
                                     break
                           
                           except Exception as e:
                                # Display error message
                                messagebox.showerror("Error", e)
                                break
                      
                      # Release video stream and close OpenCV windows
                      vs.release()
                      cv2.destroyAllWindows()
                      trigger_email()
                      # Remaining code for attendance recording...
                      if detection_counter >= 10:
                           # Record attendance for the detected real person
                           if predictions:
                                for final_id in set(predictions):
                                     final_name = getkey(final_id, student_details)
                                     print(final_name)
                                     print(final_id)
                                     
                                     late_threshold = 600
                                     absent_threshold = 900
                                     
                                     time_difference = (datetime.now() - start_time).total_seconds()
                                     print("Time Difference:", time_difference)
                                     
                                     if time_difference <= late_threshold:
                                          status = "Present"
                                     elif late_threshold < time_difference <= absent_threshold:
                                          status = "Late"
                                     else:
                                          status = "Absent"
                                     
                                     print("Late Threshold:", late_threshold)
                                     print("Absent Threshold:", absent_threshold)
                                     print("Status:", status)
                                     
                                     # Fetch department and subject data from the database
                                     cur = conn.cursor()
                                     cur.execute("SELECT department, subject FROM attendance WHERE eid = %s",
                                                 (final_id,))
                                     department_subject_result = cur.fetchone()
                                     department = department_subject_result[
                                          0] if department_subject_result else "Unknown"
                                     subject = department_subject_result[
                                          1] if department_subject_result else "Unknown"
                                     
                                     # Show attendance status message box
                                     messagebox.showinfo("Attendance Status",
                                                         "Hello {}. Your attendance is recorded .".format(
                                                              final_name))
                                     
                                     # Check if the student has a record in time in
                                     cur.execute(
                                          "SELECT * FROM report WHERE id = %s AND date = %s AND status = 'Present'",
                                          (final_id, date.today()))
                                     existing_record = cur.fetchone()
                                     
                                     if existing_record:
                                          # If the student has a record in time in, update the time
                                          cur2 = conn.cursor()
                                          cur2.execute(
                                               "UPDATE report SET time = %s WHERE id = %s AND date = %s AND status = 'Present'",
                                               (datetime.now().strftime("%H:%M:%S"), final_id, date.today()))
                                          conn.commit()
                                     else:
                                          # If the student has no record in time in, mark them as absent
                                          cur2 = conn.cursor()
                                          cur2.execute(
                                               "INSERT INTO report(id, name, department, subject, date, time, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                               (final_id, final_name, department, subject, date.today(),
                                                datetime.now().strftime("%H:%M:%S"),
                                                "Absent"))
                                          conn.commit()
                      
                      # Update attendance status for students who didn't scan during time out
                      all_student_ids = set(student_details.values())
                      students_absent_timeout = all_student_ids - set(predictions)
                      for absent_id in students_absent_timeout:
                           absent_name = getkey(absent_id, student_details)
                           absent_threshold = 1
                           time_difference = (datetime.now() - start_time).total_seconds()
                           if time_difference > absent_threshold:
                                status = "Absent"
                                cur = conn.cursor()
                                cur.execute(
                                     "UPDATE report SET status=%s, time=%s WHERE id=%s AND date=%s AND status='Present'",
                                     (status, datetime.now().strftime("%H:%M:%S"), absent_id, date.today()))
                                conn.commit()
                                messagebox.showinfo("Attendance Status",
                                                    "Hello {}. Your attendance is updated to {} for time out.".format(
                                                         absent_name, status))
                      
                      # Update attendance status for students present during time in but not recorded during time out
                      students_present_timeout = set(predictions) - all_student_ids
                      for present_id in students_present_timeout:
                           present_name = getkey(present_id, student_details)
                           status = "Absent"
                           cur = conn.cursor()
                           cur.execute(
                                "UPDATE report SET status=%s, time=%s WHERE id=%s AND date=%s AND status='Present'",
                                (status, datetime.now().strftime("%H:%M:%S"), present_id, date.today()))
                           conn.commit()
                           messagebox.showinfo("Attendance Status",
                                               "Hello {}. Your attendance is updated to {} for time out.".format(
                                                    present_name, status))
                      
                      
                      else:
                           messagebox.showinfo("No Spoof Attempts Detected", "No spoof attempts detected")
                          
                 
                 
                 else:
                      messagebox.showerror("Error",
                                           "Model files not found. Embeddings.pickle file and Recognizer.pickle file must exist within models directory.")
                
                 
                 ##################################  Function to recognize the face #############################
                 
                 ######################################## To display the attendance register report ##############################
            
            def report ():
                 report = Toplevel()
                 report.geometry("1380x660+0+0")
                 report.title("Attendance Report")
                 report.config(bg="#FF9900")
                 
                 def back ():
                      report.destroy()
                 
                 ############################################ Functions of all buttons that are used in this report window #########################################################
                 ############################################## To fetch the data from the database and display it into the app table #############################
                 
                 ########################################### To update the data  ################################################
                 
                 def clear ():
                      return True
                 
                 def export_to_excel (logged_in_username):
                      try:
                           conn = pymysql.connect(host="localhost", user="root", password="", database="recognition")
                           cur = conn.cursor()
                           
                           # Fetch username and subject from the login table based on the logged-in username
                           cur.execute("SELECT username, subject FROM login WHERE username = %s", (logged_in_username,))
                           user_info = cur.fetchone()
                           if user_info:
                                username, subject = user_info
                           else:
                                username = "N/A"
                                subject = "N/A"
                           
                           # Fetch data from the report table
                           cur.execute("SELECT * FROM report")
                           data = cur.fetchall()
                           
                           print("Fetched data:", data)  # Print fetched data for debugging
                           
                           if len(data) != 0:
                                df = pd.DataFrame(data,
                                                  columns=['ID', 'Year', 'Name', 'Date', 'Time', 'Status', 'Subject'])
                                
                                print("DataFrame created successfully.")  # Print message for debugging
                                
                                now = datetime.now()
                                current_date_time = now.strftime("%Y_%m_%d_%H_%M")
                                
                                folder = 'exports'
                                if not os.path.exists(folder):
                                     os.makedirs(folder)
                                
                                excel_filename = os.path.join(folder,
                                                              f'attendance_report_{logged_in_username}_{subject}_{current_date_time}.xlsx')
                                
                                print("Excel filename:", excel_filename)  # Print filename for debugging
                                
                                df.to_excel(excel_filename, index=False)
                                
                                print("Excel file created successfully.")  # Print message for debugging
                                
                                messagebox.showinfo("Success",
                                                    f"Data has been exported to {excel_filename} successfully. Username: {username}, Subject: {subject}")
                           else:
                                messagebox.showinfo("Information", "No data found to export.")
                           
                           conn.close()
                      except Exception as e:
                           messagebox.showerror("Error", f"An error occurred: {e}")
                 
                 # Creating the main application window
                 
                 ##################################################### To show all the datas from the database #######################################################################
                 def show_data ():
                      conn = pymysql.connect(host="localhost", user="root", password="", database="recognition")
                      cur = conn.cursor()
                      cur.execute("select * from report")
                      data = cur.fetchall()
                      if len(data) != 0:
                           report_table.delete(*report_table.get_children())
                           for row in data:
                                report_table.insert('', END, values=row)
                           conn.commit()
                      conn.close()
                 
                 ############################################ To save the csv data into mysql database ################################################################
                 
                 def delete_data ():
                      conn = pymysql.connect(host='localhost', user='root', password='', database='recognition')
                      cur = conn.cursor()
                      selected_item = report_table.selection()[0]
                      uid = report_table.item(selected_item)['values'][0]
                      print("UID is ", uid)
                      cur.execute('delete from report where id = %s', (uid))
                      conn.commit()
                      report_table.delete(selected_item)
                      messagebox.showinfo('Success', ' Data Deleted Successfully', parent=report)
                      conn.close()
                 
                 def update (rows):
                      global mydata
                      mydata = rows
                      report_table.delete(*report_table.get_children())
                      for i in rows:
                           report_table.insert('', 'end', values=i)
                 
                 def search_data ():
                      conn = pymysql.connect(host="localhost", user="root", password="", database="recognition")
                      cur = conn.cursor()
                      
                      cur.execute("select * from report where " + str(search_by.get()) + " LIKE '%" + str(
                           search_text.get()) + "%'")
                      rows = cur.fetchall()
                      if len(rows) != 0:
                           report_table.delete(*report_table.get_children())
                           for row in rows:
                                report_table.insert('', END, values=row)
                           conn.commit()
                      else:
                           messagebox.showinfo('Sorry', 'No Data Found', parent=report)
                      conn.close()
                 
                 search_by = StringVar()
                 search_text = StringVar()
                 
                 ####################################### Textfill Frame ########################################
                 text_fill = Frame(report, height=640, width=1350, bg="#202020", borderwidth="3", relief=SUNKEN)
                 text_fill.place(x=10, y=10)
                 search_label = Label(text_fill, text="Search By:", fg="white", font=("Helvetica", 15, "bold"),
                                      bg="#202020")
                 search_label.place(x=10, y=13)
                 search_combo = Combobox(text_fill, textvariable=search_by, values=['date', 'name'],
                                         state='readonly', font=("times new roman", 15), width=12)
                 search_combo.place(x=150, y=13)
                 search_entry = Entry(text_fill, textvariable=search_text, font=("Helvetica", 15), width=12)
                 search_entry.place(x=330, y=13)
                 search_btn = Button(text_fill, text="Search", bg="#FF9900", fg="white",
                                     font=("Helvetica", 15, "bold"), command=search_data, width=12)
                 search_btn.place(x=530, y=10)
                 search_today = Button(text_fill, text="Delete", bg="#FF9900", fg="white",
                                       font=("Helvetica", 15, "bold"), command=delete_data, width=12)
                 search_today.place(x=730, y=10)
                 show_btn = Button(text_fill, height="1", text="Show All", bg="#FF9900", fg="white",
                                   font=("Helvetica", 15, "bold"), command=show_data, width=12)
                 show_btn.place(x=930, y=10)
                 excelbtn = Button(text_fill, height="1", text="Generate Excel", bg="#FF9900", fg="white",
                                   font=("Helvetica", 15, "bold"), command=export_to_excel, width=12)
                 excelbtn.place(x=1130, y=10)
                 
                 ###################################### Table frame #######################################
                 
                 table_frame = Frame(text_fill, borderwidth="3", relief=GROOVE, bg="white")
                 table_frame.place(x=10, y=55, height=560, width=1325)
                 scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
                 scroll_y = Scrollbar(table_frame, orient=VERTICAL)
                 report_table = Treeview(table_frame,
                                         columns=("ID", "Year", "Name", "Date", "Time", "Subject", "Status"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
                 scroll_x.pack(side=BOTTOM, fill=X)
                 scroll_y.pack(side=RIGHT, fill=Y)
                 scroll_x.config(command=report_table.xview)
                 scroll_y.config(command=report_table.yview)
                 report_table.heading('ID', text="ID")
                 report_table.heading('Year', text="Year")
                 report_table.heading('Date', text="Date")
                 report_table.heading('Name', text="Name")
                 report_table.heading("Time", text="Time")
                 report_table.heading("Status", text="Status")
                 report_table.heading("Subject", text="Subject")
                 report_table['show'] = 'headings'
                 report_table.column("ID", width=100)
                 report_table.column("Year", width=100)
                 report_table.column("Date", width=100)
                 report_table.column("Name", width=200)
                 report_table.column("Time", width=100)
                 report_table.column("Status", width=200)
                 report_table.column("Subject", width=100)
                 report_table.pack(fill=BOTH, expand=1)
                 
                 show_data()
                 report.mainloop()
                 
                 ################################## Function to exit the attendance management form ####################################
            
            def exit ():
                 ques = messagebox.askyesnocancel("Notification", "Do you Really want to exit?",
                                                  parent=attendance)
                 if (ques == True):
                      attendance.destroy()
                 
                 #################################### Function for the face Embedding ##############################################################
            
            def face_embedding ():
                 fe = Toplevel()
                 fe.title("Extract Embeddings")
                 fe.geometry("1400x700+0+0")
                 fe.configure(bg="#202020")
                 
                 embed_title = Label(fe, text="Extract And Save Embeddings", font=("Helvetica", 30, "bold"),
                                     bg="#202020", fg="white")
                 embed_title.place(x=0, y=0, relwidth=1)
                 student_details = embedding_obj.get_student_details()
                 embeddings_model_file = os.path.join(root_dir, "models/embeddings.pickle")
                 if not os.path.exists(embeddings_model_file):
                      [image_ids, image_paths, image_arrays, names, face_ids] = embedding_obj.get_all_face_pixels(
                           student_details)
                      face_pixels = embedding_obj.normalize_pixels(imagearrays=image_arrays)
                      
                      def start_extracting_embedding (pixels):
                           embeddings = []
                           for (i, face_pixel) in enumerate(face_pixels):
                                j = i + 1
                                percent.set(str(int((j / l) * 100)) + "%")
                                text.set(str(j) + "/" + str(l) + "tasks completed")
                                pgbar["value"] = j
                                fe.update()
                                sample = np.expand_dims(face_pixel, axis=0)
                                embedding = embedding_model.predict(sample)
                                new_embedding = embedding.reshape(-1)
                                embeddings.append(new_embedding)
                           data = {"paths": image_paths, "names": names, "face_ids": face_ids,
                                   "imageIDs": image_ids, "embeddings": embeddings}
                           f = open('models/embeddings.pickle', "wb")
                           f.write(pickle.dumps(data))
                           f.close()
                           fe.after(1000, fe.destroy)
                           messagebox.showinfo("Success",
                                               "Embedding extracted successfully.. New pickle file created to store embeddings",
                                               parent=attendance)
                      
                      def back ():
                           fe.destroy()
                      
                      backbtn = Button(fe, text='Back', fg='White', bg='#FF9900', font=('Helvetica', 18, 'bold'),
                                       command=back).place(x=1250, y=1)
                      l = len(face_pixels)
                      percent = StringVar()
                      text = StringVar()
                      pgbar = Progressbar(fe, length=500, mode='determinate', maximum=l, value=0,
                                          orient=HORIZONTAL)
                      pgbar.place(x=400, y=450)
                      percentlabel = Label(fe, textvariable=percent, font=("Helvetica", 16, "bold"))
                      percentlabel.place(x=475, y=475)
                      textlabel = Label(fe, textvariable=text, font=("Helvetica", 16, "bold"))
                      textlabel.place(x=475, y=500)
                      btn = Button(fe, text="Start Extracting Embeddings", fg='white',
                                   font=("Times new roman", 20, "bold"),
                                   command=lambda: start_extracting_embedding(pixels=face_pixels), bg="#FF9900")
                      btn.place(x=450, y=550)
                      fe.mainloop()
                 
                 else:
                      [old_data, unique_names] = embedding_obj.check_pretrained_file(embeddings_model_file)
                      remaining_names = embedding_obj.get_remaining_names(student_details, unique_names)
                      data = embedding_obj.get_remaining_face_pixels(student_details, remaining_names)
                      if data != None:
                           [image_ids, image_paths, image_arrays, names, face_ids] = data
                           face_pixels = embedding_obj.normalize_pixels(imagearrays=image_arrays)
                           
                           def start_extracting_embedding (pixels):
                                embeddings = []
                                for (i, face_pixel) in enumerate(face_pixels):
                                     j = i + 1
                                     percent.set(str(int((j / l) * 100)) + "%")
                                     text.set(str(j) + "/" + str(l) + "tasks completed")
                                     pgbar["value"] = j
                                     fe.update()
                                     sample = np.expand_dims(face_pixel, axis=0)
                                     embedding = embedding_model.predict(sample)
                                     new_embedding = embedding.reshape(-1)
                                     embeddings.append(new_embedding)
                                new_data = {"paths": image_paths, "names": names, "face_ids": face_ids,
                                            "imageIDs": image_ids, "embeddings": embeddings}
                                combined_data = {"paths": [], "names": [], "face_ids": [], "imageIDs": [],
                                                 "embeddings": []}
                                combined_data["paths"] = old_data["paths"] + new_data["paths"]
                                combined_data["names"] = old_data["names"] + new_data["names"]
                                combined_data["face_ids"] = old_data["face_ids"] + new_data["face_ids"]
                                combined_data["imageIDs"] = old_data["imageIDs"] + new_data["imageIDs"]
                                combined_data["embeddings"] = old_data["embeddings"] + new_data["embeddings"]
                                
                                f = open('models/embeddings.pickle', "wb")
                                f.write(pickle.dumps(combined_data))
                                f.close()
                                fe.after(1000, fe.destroy)
                                messagebox.showinfo("Success",
                                                    "Embedding extracted successfully.. New pickle file created to store embeddings",
                                                    parent=attendance)
                           
                           def back ():
                                fe.destroy()
                           
                           backbtn = Button(fe, text='Back', fg='White', bg='#FF9900',
                                            font=('Helvetica', 18, 'bold'), command=back).place(x=1250, y=1)
                           l = len(face_pixels)
                           percent = StringVar()
                           text = StringVar()
                           pgbar = Progressbar(fe, length=500, mode='determinate', maximum=l, value=0,
                                               orient=HORIZONTAL)
                           pgbar.place(x=400, y=450)
                           percentlabel = Label(fe, textvariable=percent, font=("Helvetica", 16, "bold"))
                           percentlabel.place(x=475, y=475)
                           textlabel = Label(fe, textvariable=text, font=("Helvetica", 16, "bold"))
                           textlabel.place(x=475, y=500)
                           btn = Button(fe, text="Start Extracting Embeddings", fg='white',
                                        font=("Helvetica", 20, "bold"),
                                        command=lambda: start_extracting_embedding(pixels=face_pixels),
                                        bg="#FF9900")
                           btn.place(x=450, y=550)
                           fe.mainloop()
                      else:
                           messagebox.showinfo("Warning",
                                               "No new Student found. Embeddings already existed for these Student")
                           fe.after(1000, fe.destroy)
                 
                 def change ():
                      account = Toplevel()
                      account.geometry('500x450+200+200')
                      account.title('Admin Account')
                      account.focus_force()
                      account.grab_set()
                      account_frame = Frame(account, bg='white', height=480, width=500)
                      account_frame.pack()
                      
                      title = Label(account_frame, text="Admin Account", font=('Helvetica', 20, 'bold'),
                                    fg='black',
                                    bg='white', bd=3, relief=SUNKEN)
                      title.place(x=3, y=3, relwidth=1)
                      
                      def back ():
                           account.destroy()
                      
                      oldpass_var = StringVar()
                      newuser_var = StringVar()
                      newpass_var = StringVar()
                      backbtn = Button(account, text='Back', bg="#FF9900", fg="black",
                                       font=("Times New Roman", 13, "bold"), borderwidth=1, relief=RIDGE,
                                       command=back).place(x=445, y=7)
                      logo_icon = PhotoImage(file='Photos/logo.png', master=account)
                      admin_logo = Label(account_frame, image=logo_icon, bg='white').place(y=70, relwidth=1)
                      pass_icon = PhotoImage(file='Photos/password.png', master=account)
                      pass_logo = Label(account_frame, image=pass_icon).place(x=7, y=200)
                      pass_label = Label(account_frame, text='Old Password',
                                         font=('times new roman', 14, 'bold')).place(x=55, y=215)
                      pass_entry = Entry(account_frame, show='*', font=('times new roman', 14, 'bold'),
                                         textvariable=oldpass_var).place(x=210, y=215)
                      user_icon = PhotoImage(file='Photos/user.png', master=account)
                      user_logo = Label(account_frame, image=user_icon).place(x=7, y=265)
                      user_label = Label(account_frame, text='New Username',
                                         font=('times new roman', 14, 'bold')).place(x=55, y=275)
                      user_entry = Entry(account_frame, font=('times new roman', 14, 'bold'),
                                         textvariable=newuser_var).place(x=210, y=275)
                      newpass_logo = Label(account_frame, image=pass_icon).place(x=7, y=325)
                      newpass_label = Label(account_frame, text='New Password',
                                            font=('times new roman', 14, 'bold')).place(x=55, y=335)
                      newpass_entry = Entry(account_frame, show='*', font=('times new roman', 14, 'bold'),
                                            textvariable=newpass_var).place(x=210, y=325)
                      
                      def user_change ():
                           
                           if oldpass_var.get() == "" or newuser_var.get() == "" or newpass_var.get() == "":
                                messagebox.showerror('Error', ' All fields are Required', parent=account)
                           else:
                                conn = pymysql.connect(host='localhost', user='root', password='',
                                                       database='recognition')
                                cur = conn.cursor()
                                cur.execute('select * from login where password = %s', (oldpass_var.get()))
                                row = cur.fetchone()
                                if row == None:
                                     
                                     messagebox.showerror('Error', 'Invalid Old Password', parent=account)
                                else:
                                     cur.execute('update login set password = %s , username = %s',
                                                 (newpass_var.get(), newuser_var.get()))
                                     conn.commit()
                                     conn.close()
                                     messagebox.showinfo('Success', 'Datas Reset Successfully', parent=account)
                                     account.destroy()
                      
                      btn = Button(account_frame, text='Reset', font=('Helvetica', 14, 'bold'), width=10,
                                   bg='#FF9900', command=user_change, relief=GROOVE).place(x=240, y=380)
                      account.mainloop()
            
            def face_embedding_for_login ():
                 fe = Toplevel()
                 fe.title("Extract Embeddings")
                 fe.geometry("1400x700+0+0")
                 fe.configure(bg="#202020")
                 
                 embed_title = Label(fe, text="Extract And Save Embeddings", font=("Helvetica", 30, "bold"),
                                     bg="#202020", fg="white")
                 embed_title.place(x=0, y=0, relwidth=1)
                 
                 embedding_obj1 = LoginEmbeddingExtractor(model_path='models/facenet_keras.h5')
                 
                 embeddings_model_file = os.path.join(root_dir, "models/login_embeddings.pickle")
                 
                 if not os.path.exists(embeddings_model_file) or embedding_obj1.are_there_new_accounts(
                         embeddings_model_file):
                      login_details = embedding_obj1.get_login_details()
                      login_images = embedding_obj1.get_login_images(login_details)
                      login_face_pixels = embedding_obj1.normalize_pixels(login_images["image_paths"])
                      
                      # Check if login_face_pixels contains any elements
                      if login_face_pixels.any():
                           def start_extracting_embedding (pixels):
                                embeddings = []
                                for (i, face_pixel) in enumerate(login_face_pixels):
                                     j = i + 1
                                     percent.set(str(int((j / l) * 100)) + "%")
                                     text.set(str(j) + "/" + str(l) + " tasks completed")
                                     pgbar["value"] = j
                                     fe.update()
                                     sample = np.expand_dims(face_pixel, axis=0)
                                     embedding = embedding_model1.predict(
                                          sample)  # Make sure to define embedding_model
                                     new_embedding = embedding.reshape(-1)
                                     embeddings.append(new_embedding)
                                data = {"usernames": login_images["usernames"], "embeddings": embeddings}
                                with open(embeddings_model_file, "wb") as f:
                                     pickle.dump(data, f)
                                fe.after(1000, fe.destroy)
                                messagebox.showinfo("Success", "Embeddings extracted and saved successfully.")
                           
                           def back ():
                                fe.destroy()
                           
                           backbtn = Button(fe, text='Back', fg='White', bg='#FF9900',
                                            font=('Helvetica', 18, 'bold'),
                                            command=back).place(x=1250, y=1)
                           l = len(login_face_pixels)
                           percent = StringVar()
                           text = StringVar()
                           pgbar = Progressbar(fe, length=500, mode='determinate', maximum=l, value=0,
                                               orient=HORIZONTAL)
                           pgbar.place(x=400, y=450)
                           percentlabel = Label(fe, textvariable=percent, font=("Helvetica", 16, "bold"))
                           percentlabel.place(x=475, y=475)
                           textlabel = Label(fe, textvariable=text, font=("Helvetica", 16, "bold"))
                           textlabel.place(x=475, y=500)
                           btn = Button(fe, text="Start Extracting Embeddings", fg='white',
                                        font=("Times new roman", 20, "bold"),
                                        command=lambda: start_extracting_embedding(pixels=login_face_pixels),
                                        bg="#FF9900")
                           btn.place(x=450, y=550)
                           fe.mainloop()
                      else:
                           messagebox.showinfo("Info", "No new login images found.")
                 else:
                      messagebox.showinfo("Info",
                                          "Embeddings already exist for login accounts. No new embeddings will be extracted.")
            
            def authenticate (username, password):
                 try:
                      conn = pymysql.connect(host='localhost', user='root', password='', database='recognition')
                      cursor = conn.cursor()
                      cursor.execute('SELECT * FROM login WHERE username = %s AND password = %s',
                                     (username, password))
                      row = cursor.fetchone()
                      conn.close()
                      if row is not None:
                           return row[2]  # Return the user_type if authentication successful
                      else:
                           return None  # Return None if authentication fails
                 except pymysql.Error as e:
                      messagebox.showerror('Error', f'Database error: {e}')
                      return None
            
            def open_admin_login ():
                 username = username_var.get()
                 password = password_var.get()
                 user_type = authenticate(username, password)
                 if user_type is not None and user_type == 'admin':
                      open_admin_panel()
                 else:
                      messagebox.showerror('Error', 'You are not an admin. Please login as admin.')
            
            def open_admin_panel ():
                 attendance1 = Tk()
                 attendance1.title("Facial based Attendance system")
                 attendance1.geometry("1115x600+0+0")
                 
                 # Set background color
                 attendance1.config(bg="#202020")
                 
                 global sideframe
                 sideframe = Frame(attendance1, bg="#202020")
                 sideframe.place(x=270, y=0, width=820, height=600)
                 # Create the login frame
                 sideframe1 = Frame(attendance1, bg="#FF9900")
                 sideframe1.place(x=0, y=0, width=280, height=600)
                 
                 ######################################## Face Based Attendance Management Slider ##############################
                 
                 topic = Label(attendance1, text="Admin Acces", bg="#FF9900", fg="white",
                               font=("Helvetica", 30, "bold"))
                 topic.place(x=10, y=30)
                 
                 B9 = Button(attendance1, text="Add Instructor", font=("Helvetica", 20, "bold"),
                             fg="White", bg="#FF9900", width=15,
                             borderwidth=0, highlightthickness=0, command=open_account_creation_form, )
                 
                 B9.place(x=10, y=100)
                 
                 B11 = Button(attendance1, text="Add Student", fg="White", bg="#FF9900",
                              font=("Helvetica", 20, "bold"),
                              width=15, borderwidth=0, highlightthickness=0, command=manage_student, )
                 B11.place(x=10, y=180)
                 
                 B12 = Button(attendance1, text="Change Password", font=("Helvetica", 20, "bold"),
                              fg="White", bg="#FF9900", width=15, borderwidth=0, highlightthickness=0,
                              command=open_change_password_form, )
                 B12.place(x=10, y=260)
                 
                 B13 = Button(attendance1, text="Train Data", fg="White", bg="#FF9900",
                              font=("Helvetica", 20, "bold"),
                              width=15, borderwidth=0, highlightthickness=0, command=train, )
                 B13.place(x=10, y=420)
                 
                 B14 = Button(attendance1, text="Extract data", fg="White", bg="#FF9900",
                              font=("Helvetica", 20, "bold"),
                              width=15, borderwidth=0, highlightthickness=0, command=face_embedding)
                 B14.place(x=10, y=340)
                 
                 B15 = Button(attendance1, text="Excel attendance", fg="White", bg="#FF9900",
                              font=("Helvetica", 20, "bold"),
                              width=15, borderwidth=0, highlightthickness=0, command=open_excel_viewer)
                 B15.place(x=10, y=500)
                 
                 B16 = Button(attendance1, text="Excel attendance", fg="White", bg="#FF9900",
                              font=("Helvetica", 20, "bold"),
                              width=15, borderwidth=0, highlightthickness=0, command=face_embedding_for_login)
                 B16.place(x=10, y=580)
                 
                 B17 = Button(attendance1, text="Excel attendance", fg="White", bg="#FF9900",
                              font=("Helvetica", 20, "bold"),
                              width=15, borderwidth=0, highlightthickness=0, command=Logintrain)
                 B17.place(x=10, y=660)
                 # Create a button to open the Excel viewer
                 
                 attendance.mainloop()
            
            def open_excel_viewer ():
                 try:
                      attendance1.destroy()
                      # Create a new window to display the exported data
                      viewer_window = tk.Toplevel()
                      viewer_window.title("Exported Attendance Reports")
                      
                      def on_closing ():
                           viewer_window.destroy()
                           # Show the main window again
                           open_admin_panel()
                      
                      viewer_window.protocol("WM_DELETE_WINDOW", on_closing)
                      # Function to search files
                      def search_files ():
                           query = search_entry.get().strip().lower()
                           searched_files = [f for f in all_exported_files if query in f.lower()]
                           refresh_file_list(searched_files)
                      
                      # Function to sort files by modification time
                      def sort_files_by_date ():
                           sorted_files = sorted(all_exported_files,
                                                 key=lambda x: os.path.getmtime(os.path.join(export_folder, x)),
                                                 reverse=True)
                           refresh_file_list(sorted_files)
                      
                      # Function to refresh the file list
                      def refresh_file_list (file_list):
                           for widget in files_frame.winfo_children():
                                widget.destroy()
                           
                           if not file_list:
                                label = tk.Label(files_frame, text="No matching files found.",
                                                 font=("Helvetica", 12))
                                label.pack(pady=20)
                           else:
                                for file_name in file_list:
                                     def open_file (filename):
                                          os.startfile(os.path.join(export_folder, filename))
                                     
                                     # Create a clickable label for each file
                                     label = tk.Label(files_frame, text=file_name, font=("Helvetica", 12), fg="blue",
                                                      cursor="hand2")
                                     label.pack()
                                     
                                     # Bind the label to open the file when clicked
                                     label.bind("<Button-1>", lambda event, filename=file_name: open_file(filename))
                      
                      # Create a frame to hold search and sort buttons
                      # Create a frame to hold search and sort buttons with background color
                      button_frame = tk.Frame(viewer_window, bg="#202020")
                      button_frame.pack(side="top", fill="x")
                      
                      # Entry for search query
                      search_entry = tk.Entry(button_frame, font=("Helvetica", 12), bg="#202020", fg="white")
                      search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
                      
                      # Search button
                      search_button = tk.Button(button_frame, text="Sort by Date", font=("Helvetica", 12),
                                                command=search_files, bg="#FF9900", fg="black")
                      search_button.grid(row=0, column=2, padx=5, pady=10)
                      
                      # Sort button
                      sort_button = tk.Button(button_frame, text="Search", font=("Helvetica", 12),
                                              command=sort_files_by_date, bg="#FF9900", fg="black")
                      sort_button.grid(row=0, column=1, padx=5, pady=10)
                      
                      # Create a frame to display the list of exported Excel files
                      files_frame = tk.Frame(viewer_window, width=1000, height=600)  # Set width and height
                      files_frame.pack_propagate(0)  # Prevent resizing based on contents
                      files_frame.pack(fill='both', expand=True)
                      files_frame.configure(bg="white")  # Set background color of the main frame
                      
                      # Get a list of azll exported Excel files
                      export_folder = 'exports'
                      all_exported_files = [f for f in os.listdir(export_folder) if f.endswith('.xlsx')]
                      
                      # Initially display all files
                      refresh_file_list(all_exported_files)
                      
                      def on_closing ():
                           viewer_window.destroy()
                           # Show the main window again
                           open_admin_panel()
                      
                      viewer_window.protocol("WM_DELETE_WINDOW", on_closing)
                 except Exception as e:
                      # Show error message if any error occurs
                      messagebox.showerror("Error", f"An error occurred: {e}")
            
            def create_account (username, password, user_type, subject=None):
                 try:
                      # Connect to the database
                      conn = pymysql.connect(host="localhost", user="root", password="", database="recognition")
                      
                      # Create a cursor object to execute queries
                      with conn.cursor() as cursor:
                           # SQL query to insert data into the database
                           if subject:
                                sql = "INSERT INTO login (username, password, user_type, subject) VALUES (%s, %s, %s, %s)"
                                cursor.execute(sql, (username, password, user_type, subject))
                           else:
                                sql = "INSERT INTO login (username, password, user_type) VALUES (%s, %s, %s)"
                                cursor.execute(sql, (username, password, user_type))
                      
                      # Commit changes to the database
                      conn.commit()
                      
                      # Face capture
                      capture_face_images(username)
                      
                      messagebox.showinfo("Success", "Account created successfully!")
                 except pymysql.Error as e:
                      messagebox.showerror("Error", f"Error creating account: {e}")
                 
                 # Function to capture face images for a user
            
            def capture_face_images (username):
                 try:
                      # Create directory if not exists
                      input_directory = os.path.join('dataset_login', username)
                      if not os.path.exists(input_directory):
                           os.makedirs(input_directory, exist_ok=True)
                      
                      # Capture face images
                      count = 1
                      print("[INFO] starting video stream...")
                      video_capture = cv2.VideoCapture(0)
                      while count <= 100:
                           try:
                                check, frame = video_capture.read()
                                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                                for (x, y, w, h) in faces:
                                     face = frame[y - 5:y + h + 5, x - 5:x + w + 5]
                                     resized_face = cv2.resize(face, (160, 160))
                                     cv2.imwrite(os.path.join(input_directory, username + str(count) + '.jpg'),
                                                 resized_face)
                                     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                                     count += 1
                                
                                cv2.imshow("Frame", frame)
                                key = cv2.waitKey(1)
                                if key == ord('q'):
                                     break
                           except Exception as e:
                                pass
                      video_capture.release()
                      cv2.destroyAllWindows()
                 
                 except Exception as e:
                      messagebox.showerror("Error", f"Error capturing face images: {e}")
            
            def submit_form (username_entry, password_entry, user_type_entry, subject_entry=None):
                 username = username_entry.get()
                 password = password_entry.get()
                 user_type = user_type_entry.get()
                 subject = subject_entry.get() if subject_entry else None
                 
                 if not username or not password or not user_type:
                      messagebox.showerror("Error", "Please fill in all the fields")
                 else:
                      create_account(username, password, user_type, subject)
            
            def open_account_creation_form ():
                 manage_student_frame1 = Frame(sideframe, bg="#202020")
                 manage_student_frame1.pack(fill=BOTH, expand=True)
                 
                 username_label = Label(manage_student_frame1, text="Username", fg="white", bg="#202020",
                                        font=("Helvetica", 20, "bold"))
                 username_label.place(x=35, y=30)
                 username_entry = Entry(manage_student_frame1, fg="white", bg="#202020",
                                        font=("Helvetica", 20, "bold"))
                 username_entry.place(x=35, y=130)
                 
                 password_label = Label(manage_student_frame1, text="Password:", fg="white", bg="#202020",
                                        font=("Helvetica", 20, "bold"))
                 password_label.place(x=35, y=230)
                 password_entry = Entry(manage_student_frame1, show="*", fg="white", bg="#202020",
                                        font=("Helvetica", 20, "bold"))
                 password_entry.place(x=35, y=330)
                 
                 user_type_label = Label(manage_student_frame1, text="User Type:", fg="white", bg="#202020",
                                         font=("Helvetica", 20, "bold"))
                 user_type_label.place(x=435, y=30)
                 
                 user_type_entry = Entry(manage_student_frame1, fg="white", bg="#202020",
                                         font=("Helvetica", 20, "bold"))
                 user_type_entry.place(x=435, y=130)
                 
                 subject_label = Label(manage_student_frame1, text="Subject:", fg="white", bg="#202020",
                                       font=("Helvetica", 20, "bold"))
                 subject_label.place(x=435, y=230)
                 
                 subject_entry = Entry(manage_student_frame1, fg="white", bg="#202020",
                                       font=("Helvetica", 20, "bold"))
                 subject_entry.place(x=435, y=330)
                 
                 submit_button = Button(manage_student_frame1, text="Submit", fg="White", bg="#FF9900",
                                        font=("Helvetica", 20, "bold"), width=10,
                                        command=lambda: submit_form(username_entry, password_entry,
                                                                    user_type_entry, subject_entry))
                 submit_button.place(x=35, y=430)
                 
                 # Call the function to open the account creation form immediately
            
            def show_account_creation_form ():
                 open_account_creation_form()
            
            def change_password (username, current_password, new_password):
                 try:
                      with conn.cursor() as cursor:
                           # Check if the current password is correct
                           cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s",
                                          (username, current_password))
                           user = cursor.fetchone()
                           if user:
                                # Update the password
                                cursor.execute("UPDATE login SET password = %s WHERE username = %s",
                                               (new_password, username))
                                conn.commit()
                                messagebox.showinfo("Success", "Password changed successfully!")
                           else:
                                messagebox.showerror("Error", "Incorrect current password")
                 except pymysql.Error as e:
                      messagebox.showerror("Error", f"Error changing password: {e}")
            
            def submit_form1 (username_entry, current_password_entry, new_password_entry):
                 username = username_entry.get()
                 current_password = current_password_entry.get()
                 new_password = new_password_entry.get()
                 change_password(username, current_password, new_password)
            
            def open_change_password_form ():
                 change_password_frame = Tk()
                 change_password_frame.title("Change Password")
                 change_password_frame.geometry("1115x600+0+0")
                 change_password_frame.config(bg="#202020")
                 
                 username_label = Label(change_password_frame, text="Username", fg="white", bg="#202020",
                                        font=("Helvetica", 20, "bold"))
                 username_label.place(x=35, y=30)
                 username_entry = Entry(change_password_frame, fg="white", bg="#202020",
                                        font=("Helvetica", 20, "bold"))
                 username_entry.place(x=35, y=100)
                 
                 current_password_label = Label(change_password_frame, text="Current Password:", fg="white",
                                                bg="#202020",
                                                font=("Helvetica", 20, "bold"))
                 current_password_label.place(x=35, y=170)
                 current_password_entry = Entry(change_password_frame, show="*", fg="white", bg="#202020",
                                                font=("Helvetica", 20, "bold"))
                 current_password_entry.place(x=35, y=240)
                 
                 new_password_label = Label(change_password_frame, text="New Password:", fg="white", bg="#202020",
                                            font=("Helvetica", 20, "bold"))
                 new_password_label.place(x=35, y=310)
                 new_password_entry = Entry(change_password_frame, show="*", fg="white", bg="#202020",
                                            font=("Helvetica", 20, "bold"))
                 new_password_entry.place(x=35, y=380)
                 
                 submit_button = Button(change_password_frame, text="Submit", fg="white", bg="#FF9900", width=10,
                                        font=("Helvetica", 20, "bold"),
                                        command=lambda: submit_form1(username_entry, current_password_entry,
                                                                     new_password_entry))
                 submit_button.place(x=35, y=450)
                 
                 # Define the function to show the change password form
            
            def show_change_password_form ():
                 open_change_password_form()
            
            def detect_hands ():
                 handsvm = cv2.CascadeClassifier('handraising/haarcascade_hand.xml')
                 palmsvm = cv2.CascadeClassifier('handraising/rpalm_cascade.xml')
                 handsvm1 = cv2.CascadeClassifier('handraising/palm_v4.xml')
                 handsvm2 = cv2.CascadeClassifier('handraising/palm.xml')
                 
                 def play_sound ():
                      winsound.Beep(500, 300)
                 
                 def detect (gray, frame):
                      hands = handsvm.detectMultiScale(gray, 1.3, 5)
                      palm = palmsvm.detectMultiScale(gray, 1.3, 5)
                      hands1 = handsvm1.detectMultiScale(gray, 1.3, 5)
                      hands2 = handsvm2.detectMultiScale(gray, 1.3, 5)
                      
                      for (x, y, w, h) in hands2:
                           cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                           roi_gray = gray[y:y + h, x:x + w]
                           roi_color = frame[y:y + h, x:x + w]
                      
                      for (x, y, w, h) in hands:
                           cv2.putText(frame, 'hand raising', (x, y), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
                           cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 2)
                      
                      for (x, y, w, h) in hands1:
                           cv2.putText(frame, 'hand raising', (x, y), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
                           cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 2)
                           play_sound()
                      
                      for (x, y, w, h) in palm:
                           cv2.putText(frame, 'hand raising', (x, y), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
                           cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 2)
                           play_sound()
                      
                      return frame
                 
                 # Creating a frameless window
                 window = "Frameless Window"
                 cv2.namedWindow(window, cv2.WINDOW_NORMAL)
                 cv2.setWindowProperty(window, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                 cv2.setWindowProperty(window, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_GUI_NORMAL)
                 cv2.moveWindow(window, 400, 130)
                 cv2.resizeWindow(window, 700, 460)
                 
                 # Initializing the camera
                 video_capture = cv2.VideoCapture(1)  # 0 for internal camera, 1 for external camera
                 
                 while True:
                      _, frame = video_capture.read()
                      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                      
                      # Edge detection
                      lower = 115
                      upper = 235
                      canvas = cv2.Canny(gray, lower, upper)
                      
                      # Hand detection
                      detected_frame = detect(gray, frame)
                      
                      # Displaying the detected frames in the frameless window
                      cv2.imshow(window, detected_frame)
                      
                      # Press 'q' to break the loop
                      if cv2.waitKey(1) & 0xFF == ord('q'):
                           break
                 
                 video_capture.release()
                 cv2.destroyAllWindows()
                 
                 ########################################## Facial Based Attendance system page ##################################
            
            global attendance
            attendance = Tk()
            attendance.title("Facial based Attendance system")
            attendance.geometry("1115x600+0+0")
            
            # Set background color
            attendance.config(bg="#202020")
            global sideframe4
            sideframe4 = Frame(attendance, bg="#202020")
            sideframe4.place(x=350, y=50, width=820, height=600)
            
            ######################################## Face Based Attendance Management Slider ##############################
            def faceslider ():
                 global count, text
                 if (count >= len(manage)):
                      count = -1
                      text = ''
                      topic.config(text=text)
                 else:
                      text = text + manage[count]
                      topic.config(text=text)
                      count += 1
                 topic.after(200, faceslider)
            
            manage = username_var.get()
            topic = Label(attendance, text="Instructor: " + "[" + username + "]", bg="#202020", fg="white",
                          font=("Helvetica", 30, "bold"))
            topic.place(x=20, y=40)
            
            B1 = Button(attendance, text="ATTENDANCE REPORT", font=("Helvetica", 20, "bold"),
                        fg="White", bg="#FF9900", width=20, command=report, )
            B1.place(x=20, y=100)
            
            B2 = Button(attendance, text="TIME IN", font=("Helvetica", 20, "bold"),
                        fg="White", bg="#FF9900", width=9, command=time_in, )
            B2.place(x=20, y=180)
            
            B3 = Button(attendance, text="TIME OUT", font=("Helvetica", 20, "bold"),
                        fg="White", bg="#FF9900", width=10, command=time_out, )
            B3.place(x=190, y=180)
            
            B4 = Button(attendance, text="DETECT RAISING", font=("Helvetica", 20, "bold"),
                        fg="White", bg="#FF9900", width=20, command=detect_hands)
            B4.place(x=20, y=260)
            
            B5 = Button(attendance, text="SEND EMAIL", font=("Helvetica", 20, "bold"),
                        fg="White", bg="#FF9900", width=20, command=trigger_email)
            B5.place(x=20, y=340)
            
            B6 = Button(attendance, text="LOGOUT", font=("Helvetica", 20, "bold"),
                        fg="White", bg="#FF9900", width=9, command=exit, )
            B6.place(x=20, y=500)
            
            B7 = Button(attendance, text="'Q' TO STOP", font=("Helvetica", 20, "bold"),
                        fg="White", bg="#FF9900", width=10, )
            B7.place(x=190, y=500)
            
            B8 = Button(attendance, text="Admin Access", fg="White", bg="#FF9900",
                        font=("Helvetica", 20, "bold"),
                        width=20, command=open_admin_login, )
            B8.place(x=20, y=420)
            
            attendance.mainloop()
    except pymysql.err.OperationalError as e:
        messagebox.showerror("Error",
                             "Sql Connection Error... Open Xamp Control Panel and then start MySql Server ")
    except Exception as e:
         print(e)
         messagebox.showerror("Error", "Close all the windows and restart your program")

def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg='grey')

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg='black')

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg='grey')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def add_password_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg='grey')

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg='black', show='*')

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg='grey', show='')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    
def tick():
        time_string = time.strftime("%H:%M:%S")
        date_string = time.strftime("%d:%m:%Y")
        # print(time_string , date_string)
        clock.config(text="Time :" + time_string + "\n" + "Date :" + date_string)
        clock.after(200, tick)

        ########################### Admin login page form ####################################

face.configure(background="#FF9900")

login_frame_width = 800
login_frame_height = 400

# Create the login frame
login_frame = Frame(face, bg="#202020")
login_frame.place(x=300, y=200, width=login_frame_width, height=login_frame_height)

clock = Label(login_frame, font=("Helvetica", 15, "bold"), bg="#202020", fg="White", relief=GROOVE)
clock.place(x=120, y=20)
tick()
    # Load logo image
logo_image = PhotoImage(file="Photos/one.png", master=login_frame)
    # Create label for logo image and position it in the grid
logo_label = Label(login_frame, image=logo_image, bd=0)
logo_label.place(x=40, y=80)

    # Username label and entry
user_label = Label(login_frame, text="Enter your Classroom", bg="#202020", fg="#FF9900",
                       font=("Helvetica", 25, "bold"))
user_label.place(x=400, y=40)

user_entry = Entry(login_frame, font=("Helvetica", 25, "bold"), relief=GROOVE, textvariable=username_var,
                       bg="white")
user_entry.place(x=400, y=120)
add_placeholder(user_entry, "Username")


    # Password label and entry
password_label = Label(login_frame, text="input your account to start the class", bg="#202020", fg="White",
                           font=("Helvetica", 15, "bold"))
password_label.place(x=400, y=80)

password_entry = Entry(login_frame, font=("Helvetica", 25, "bold"), relief=GROOVE, #show="*",
                           textvariable=password_var, bg="white")
password_entry.place(x=400, y=180)
add_password_placeholder(password_entry, "Password")

    # Submit button
submit_btn = Button(login_frame, text="Login", width=16, activebackground="blue", activeforeground="white",
                        command=login, font=("Helvetica", 22, "bold"), fg="White", relief=GROOVE, bg="#FF9900")
submit_btn.place(x=400, y=240)
image_path = 'Photos/login.jpg'
pil_image = Image.open(image_path)
login_image1 = ImageTk.PhotoImage(pil_image)

# Create the button with the image
login_button = Button(login_frame, image=login_image1, command=lambda: face_recognition_login(username_var.get()),
                      borderwidth=0, highlightthickness=0)
login_button.place(x=705, y=240)

# Keep a reference to the image
login_button.image = login_image1

# Keep a reference to the image
# Start the main loop
face.mainloop()


# Run the main event loop
