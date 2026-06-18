import csv
import datetime
import os
from tkinter import messagebox, ttk
import tkinter as tk

DATA_FILE = "clinic_queue.csv"

# ==========================================
# USER ACCOUNTS
# ==========================================

USERS = {
    "admin": "admin123",
    "reception": "clinic123",
    "nurse": "nurse123"
}


# ==========================================
# FILE HANDLING FUNCTIONS
# ==========================================

def load_patients():
    patients = []

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                patients.append(row)

    return patients


def save_patient(name, age, complaint, priority):

    file_exists = os.path.exists(DATA_FILE)

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Time",
                "Name",
                "Age",
                "Complaint",
                "Priority",
                "Status"
            ])

        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        writer.writerow([
            time_now,
            name,
            age,
            complaint,
            priority,
            "Waiting"
        ])


def rewrite_csv(data):

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Time",
            "Name",
            "Age",
            "Complaint",
            "Priority",
            "Status"
        ])

        for row in data:
            writer.writerow([
                row["Time"],
                row["Name"],
                row["Age"],
                row["Complaint"],
                row["Priority"],
                row["Status"]
            ])

    # ==========================================
    # VALIDATION
    # ==========================================


def validate_input(name, age, complaint):
    if name.strip() == "":
        messagebox.showerror("Error", "Patient name required")
        return False

    if not age.isdigit():
        messagebox.showerror("Error", "Age must be a number")
        return False

    if int(age) < 1 or int(age) > 120:
        messagebox.showerror("Error", "Invalid age")
        return False

    if complaint.strip() == "":
        messagebox.showerror("Error", "Complaint required")
        return False

    return True

    # ==========================================
    # PRIORITY CALCULATION
    # ==========================================


def calculate_priority(age, complaint):
    complaint = complaint.lower()

    emergency_words = [
        "bleeding",
        "accident",
        "chest pain",
        "unconscious",
        "difficulty breathing"
    ]

    if any(word in complaint for word in emergency_words):
        return "Emergency"

    elif int(age) < 5 or int(age) > 65:
        return "High"

    else:
        return "Normal"

# ==========================================
# LOGIN SYSTEM
# ==========================================


def login():

    username = username_entry.get()
    password = password_entry.get()

    if username in USERS and USERS[username] == password:

        login_window.destroy()
        open_dashboard()

    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid Username or Password"
        )


login_window = tk.Tk()

login_window.title("Salone Clinic Login")
login_window.geometry("400x300")
login_window.configure(bg="#e8f5e9")

title = tk.Label(
    login_window,
    text="Salone Clinic Login",
    font=("Arial", 16, "bold"),
    bg="#e8f5e9"
)

title.pack(pady=20)

# noinspection PyArgumentList
tk.Label(
    login_window,
    text="Username:"
).pack()

username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

# noinspection PyArgumentList
tk.Label(
    login_window,
    text="Password:"
).pack()

password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=5)

tk.Button(
    login_window,
    text="Login",
    bg="green",
    fg="white",
    width=15,
    command=login
).pack(pady=20)

# ==========================================
# DASHBOARD
# ==========================================

def update_dashboard():

    patients = load_patients()

    total = len(patients)

    emergency = sum(
        1 for p in patients
        if p["Priority"] == "Emergency"
    )

    high = sum(
        1 for p in patients
        if p["Priority"] == "High"
    )

    normal = sum(
        1 for p in patients
        if p["Priority"] == "Normal"
    )

    total_label.config(text=f"Total Patients\n{total}")
    emergency_label.config(text=f"Emergency\n{emergency}")
    high_label.config(text=f"High Priority\n{high}")
    normal_label.config(text=f"Normal\n{normal}")


def show_dashboard():
    """Switch view to dashboard"""
    global dashboard_frame, patient_frame
    dashboard_frame.tkraise()


def show_patient_manager():
    """Switch view to patient manager"""
    global dashboard_frame, patient_frame
    patient_frame.tkraise()


def open_dashboard():

    global dashboard
    global dashboard_frame
    global patient_frame
    global total_label
    global emergency_label
    global high_label
    global normal_label
    global entry_name
    global entry_age
    global entry_complaint
    global queue_table
    global search_entry

    dashboard = tk.Tk()

    dashboard.title("Salone Clinic System")
    dashboard.geometry("1100x650")

    # ========== DASHBOARD FRAME ==========
    dashboard_frame = tk.Frame(dashboard)
    dashboard_frame.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(
        dashboard_frame,
        text="SALONE CLINIC DASHBOARD",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    card_frame = tk.Frame(dashboard_frame)
    card_frame.pack(pady=20)

    total_label = tk.Label(
        card_frame,
        width=18,
        height=5,
        bg="#2196F3",
        fg="white"
    )

    emergency_label = tk.Label(
        card_frame,
        width=18,
        height=5,
        bg="#f44336",
        fg="white"
    )

    high_label = tk.Label(
        card_frame,
        width=18,
        height=5,
        bg="#ff9800",
        fg="white"
    )

    normal_label = tk.Label(
        card_frame,
        width=18,
        height=5,
        bg="#4CAF50",
        fg="white"
    )

    total_label.grid(row=0, column=0, padx=10)
    emergency_label.grid(row=0, column=1, padx=10)
    high_label.grid(row=0, column=2, padx=10)
    normal_label.grid(row=0, column=3, padx=10)

    update_dashboard()

    tk.Button(
        dashboard_frame,
        text="Open Patient Manager",
        width=25,
        bg="green",
        fg="white",
        command=show_patient_manager
    ).pack(pady=20)

    tk.Button(
        dashboard_frame,
        text="Exit",
        width=20,
        bg="red",
        fg="white",
        command=dashboard.destroy
    ).pack()

    # ========== PATIENT FRAME ==========
    patient_frame = tk.Frame(dashboard)
    patient_frame.place(x=0, y=0, relwidth=1, relheight=1)

    # Title
    tk.Label(
        patient_frame,
        text="PATIENT MANAGEMENT",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    # =============================
    # INPUT SECTION
    # =============================

    input_frame = tk.LabelFrame(
        patient_frame,
        text="Patient Registration",
        padx=10,
        pady=10
    )

    input_frame.pack(fill="x", padx=10, pady=10)

    tk.Label(input_frame, text="Patient Name").grid(
        row=0,
        column=0,
        padx=5,
        pady=5
    )

    entry_name = tk.Entry(input_frame, width=30)
    entry_name.grid(row=0, column=1)

    tk.Label(input_frame, text="Age").grid(
        row=1,
        column=0,
        padx=5,
        pady=5
    )

    entry_age = tk.Entry(input_frame, width=10)
    entry_age.grid(row=1, column=1)

    tk.Label(input_frame, text="Complaint").grid(
        row=2,
        column=0,
        padx=5,
        pady=5
    )

    entry_complaint = tk.Entry(input_frame, width=40)
    entry_complaint.grid(row=2, column=1)

    # =============================
    # BUTTONS
    # =============================

    button_frame = tk.Frame(patient_frame)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Add Patient",
        bg="#4CAF50",
        fg="white",
        width=15,
        command=add_patient
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame,
        text="Mark Served",
        bg="#2196F3",
        fg="white",
        width=15,
        command=mark_served
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        button_frame,
        text="Delete Patient",
        bg="#f44336",
        fg="white",
        width=15,
        command=delete_patient
    ).grid(row=0, column=2, padx=5)

    tk.Button(
        button_frame,
        text="Back to Dashboard",
        bg="#FFC107",
        fg="black",
        width=20,
        command=show_dashboard
    ).grid(row=0, column=3, padx=5)

    # =============================
    # SEARCH BAR
    # =============================

    search_frame = tk.Frame(patient_frame)
    search_frame.pack(pady=10)

    tk.Label(
        search_frame,
        text="Search Patient:"
    ).pack(side="left")

    search_entry = tk.Entry(
        search_frame,
        width=30
    )

    search_entry.pack(side="left", padx=5)

    tk.Button(
        search_frame,
        text="Search",
        command=search_patient
    ).pack(side="left")

    tk.Button(
        search_frame,
        text="Refresh",
        command=refresh_queue
    ).pack(side="left", padx=5)

    # =============================
    # TABLE
    # =============================

    columns = (
        "Time",
        "Name",
        "Age",
        "Complaint",
        "Priority",
        "Status"
    )

    queue_table = ttk.Treeview(
        patient_frame,
        columns=columns,
        show="headings"
    )

    for col in columns:
        queue_table.heading(col, text=col)
        queue_table.column(col, width=150)

    queue_table.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    refresh_queue()

    # Start with dashboard view
    show_dashboard()

    dashboard.mainloop()

# ==========================================
# ADD PATIENT
# ==========================================

def add_patient():

    name = entry_name.get()
    age = entry_age.get()
    complaint = entry_complaint.get()

    if not validate_input(
        name,
        age,
        complaint
    ):
        return

    priority = calculate_priority(
        age,
        complaint
    )

    save_patient(
        name,
        age,
        complaint,
        priority
    )

    messagebox.showinfo(
        "Success",
        "Patient added successfully"
    )

    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_complaint.delete(0, tk.END)

    refresh_queue()
    update_dashboard()


# ==========================================
# REFRESH TABLE
# ==========================================

def refresh_queue():

    for item in queue_table.get_children():
        queue_table.delete(item)

    patients = load_patients()

    for p in patients:

        queue_table.insert(
            "",
            "end",
            values=(
                p["Time"],
                p["Name"],
                p["Age"],
                p["Complaint"],
                p["Priority"],
                p["Status"]
            )
        )

# ==========================================
# SEARCH PATIENT
# ==========================================

def search_patient():

    keyword = search_entry.get().lower()

    for item in queue_table.get_children():
        queue_table.delete(item)

    patients = load_patients()

    for p in patients:

        if keyword in p["Name"].lower():

            queue_table.insert(
                "",
                "end",
                values=(
                    p["Time"],
                    p["Name"],
                    p["Age"],
                    p["Complaint"],
                    p["Priority"],
                    p["Status"]
                )
            )

# ==========================================
# MARK SERVED
# ==========================================

def mark_served():

    selected = queue_table.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Select a patient"
        )

        return

    values = queue_table.item(
        selected[0]
    )["values"]

    patient_name = values[1]

    patients = load_patients()

    for p in patients:

        if p["Name"] == patient_name:
            p["Status"] = "Served"

    rewrite_csv(patients)

    refresh_queue()

    messagebox.showinfo(
        "Updated",
        "Patient marked as served"
    )

# ==========================================
# DELETE PATIENT
# ==========================================

def delete_patient():

    selected = queue_table.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Select a patient"
        )

        return

    values = queue_table.item(
        selected[0]
    )["values"]

    patient_name = values[1]

    patients = load_patients()

    new_list = []

    for p in patients:

        if p["Name"] != patient_name:
            new_list.append(p)

    rewrite_csv(new_list)

    refresh_queue()
    update_dashboard()

    messagebox.showinfo(
        "Deleted",
        "Patient removed successfully"
    )

# ==========================================
# START PROGRAM
# ==========================================

login_window.mainloop()
