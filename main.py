from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import requests
import pandas as pd
from PIL import Image, ImageTk

from PIL import ImageTk
from PIL import Image
import tkinter
import numpy as np
import tkinter as tk

import pyautogui
import sys
import time
from tkinter.filedialog import asksaveasfilename
from PIL import Image, ImageTk
import pandas as pd


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login With Your Account")
        self.root.geometry("320x250+600+250")
        self.root.configure(bg='#2E2E2E')

        title = Label(self.root, text="    SIGN IN", padx=10, compound=LEFT, font=("Goudy Old Style", 40, "bold"), bg="#222A35", fg="Yellow", anchor="w")
        title.place(x=0, y=0, relwidth=1)

        self.label_username = Label(root, text="Username:")
        self.label_password = Label(root, text="Password:")
        self.entry_username = Entry(root)
        self.entry_password = Entry(root, show="*")

        self.label_username.place(x=50, y=88)
        self.entry_username.place(x=120, y=90)
        self.label_password.place(x=50, y=120)
        self.entry_password.place(x=120, y=120)

        self.login_button = Button(root, text="Login", command=self.login)
        self.login_button.place(x=135, y=160)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        admin_username = "admin"
        admin_password = "admin"  # Change this to your admin password

        if username == admin_username and password == admin_password:
            tkinter.messagebox.showinfo("Login", "Login Successful!")
            self.root.destroy()  # Close the login window
            root_app = Tk()  # Create a new Tk instance for the app window
            app = BulkSMSApp(root_app)
            root_app.mainloop()  # Open the main application window
        else:
            tkinter.messagebox.showerror("Login Error", "Invalid username or password")


class BulkSMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulk SMS Sender")
        self.root.geometry("1080x650+200+50")
        self.root.resizable(False, False)
        self.root.config(bg="White")
        self.api_key = "Uk6k94ekDAAgBASrx9Cf"

        # Icons
        image = Image.open('email.png')
        img = image.resize((50, 50))
        self.email_icon = ImageTk.PhotoImage(img)

        image2 = Image.open('setting.png')
        img2 = image2.resize((60, 60))
        self.setting = ImageTk.PhotoImage(img2)

        # Title
        title = Label(self.root, text="Bulk SMS Sender", image=self.email_icon, padx=10, compound=LEFT,font=("Goudy Old Style", 48, "bold"), bg="#222A35", fg="Yellow", anchor="w")
        title.place(x=0, y=0, relwidth=1)

        dev = Label(self.root, text="Developed by Kawsar", font=("Times New Roman", 30, "bold"),bg="#222A35", fg="White")
        dev.place(x=650, y=15)

        des = Label(self.root,text="Use Excel File to Send Bulk SMS at Once, With Just One Click. Ensure The Number Column Name Be Phone",font=("Calibri (Body)", 14), bg="#FFD966", fg="Black")
        des.place(x=0, y=82, relwidth=1)

        to = Label(self.root, text="Phone Number", font=("times new roman", 18), bg="white")
        to.place(x=50, y=220)

        msg = Label(self.root, text="MESSAGE", font=("times new roman", 18), bg="white")
        msg.place(x=50, y=320)

        self.txt_to = Entry(self.root, font=("times new roman", 14), bg="lightyellow")
        self.txt_to.place(x=400, y=220, width=320, height=35)

        self.brwose = Button(self.root, text="Import", font=("times new roman", 18, "bold"),command=self.import_from_excel, bg="#8FAADC", activebackground="#8FAADC",activeforeground="#262626", fg="#262626", cursor="hand2")
        self.brwose.place(x=750, y=220, width=100, height=35)

        self.txt_msg = Text(self.root, font=("times new roman", 14), bg="lightyellow")
        self.txt_msg.place(x=400, y=320, width=580, height=160)

        self.send_button = Button(self.root, text="Send SMS", font=("times new roman", 18, "bold"),command=self.send_sms, bg="#8FAADC", activebackground="#8FAADC",activeforeground="#262626", fg="#262626")
        self.send_button.place(x=780, y=530)

        self.clear_button = Button(self.root, text="Clear", font=("times new roman", 18, "bold"),command=self.clear_fields, bg="#8FAADC", activebackground="#8FAADC",activeforeground="#262626", fg="#262626")
        self.clear_button.place(x=650, y=530)
        
        
    def clear_fields(self):
        self.txt_to.delete(0, END)
        self.txt_msg.delete("1.0", END)


    def import_from_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                data = pd.read_excel(file_path)
                if 'Phone' in data.columns:
                    phone_numbers = data['Phone'].astype(str).tolist()
                    self.txt_to.delete(0, END)
                    self.txt_to.insert(0, ', '.join(phone_numbers))
                else:
                    messagebox.showerror("Error", "Excel file must contain a 'Phone' column.")
            except Exception as e:
                messagebox.showerror("Error", f"Error importing data from Excel: {str(e)}")

    def send_sms(self):
        phone_numbers = self.txt_to.get()
        message = self.txt_msg.get("1.0", "end-1c")

        if not phone_numbers or not message:
            messagebox.showerror("Error", "Phone numbers and message are required.")
            return

        phone_numbers = [pn.strip() for pn in phone_numbers.split(",")]

        for phone_number in phone_numbers:
            try:
                # Construct the API URL with the provided parameters
                api_url = f"http://bulksmsbd.net/api/smsapi?api_key={self.api_key}&type=text&number={phone_number}&senderid=8809617613090&message={message}"

                response = requests.get(api_url)
                if response.status_code == 200:
                    messagebox.showinfo("Success", f"SMS sent successfully .")
                else:
                    messagebox.showerror("Error", f"Failed to send SMS .")
            except Exception as e:
                messagebox.showerror("Error", f"Error sending SMS to : {str(e)}")


if __name__ == "__main__":
    root = Tk()
    login_window = LoginWindow(root)
    root.mainloop()