import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import csv
import os

# File to store patient records
DATA_FILE = "clinic_queue.csv"


# === USER-DEFINED FUNCTIONS ===

def load_patients():
    """Load patients from CSV file. Handles multiple records."""
    patients = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                patients.append(row)
    return patients


def save_patient(name, age, complaint, priority):
    """Save new patient to CSV. Validates input first."""
    if not validate_input(name, age, complaint):
        return False

    file_exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Time', 'Name', 'Age', 'Complaint', 'Priority', 'Status'])

        time = datetime.datetime.now().strftime("%H:%M:%S")
        writer.writerow([time, name, age, complaint, priority, 'Waiting'])
    return True


def validate_input(name, age, complaint):
    """Validate GUI input - required for marks"""
    if name.strip() == "":
        messagebox.showerror("Error", "Patient name cannot be empty")
        return False
    if not age.isdigit() or int(age) < 1 or int(age) > 120:
        messagebox.showerror("Error", "Age must be a number between 1-120")
        return False
    if complaint.strip() == "":
        messagebox.showerror("Error", "Complaint cannot be empty")
        return False
    return True


def calculate_priority(age, complaint):
    """Apply logic: kids, elderly, emergencies get higher priority"""
    complaint = complaint.lower()
    emergency_keywords = ['bleeding', 'unconscious', 'chest pain', 'difficulty breathing', 'accident']

    if any(word in complaint for word in emergency_keywords):
        return "Emergency"
    elif int(age) < 5 or int(age) > 65:
        return "High"
    else:
        return "Normal"


def refresh_queue():
    """Display all patients in output area - uses loop"""
    queue_list.delete(*queue_list.get_children())
    patients = load_patients()

    for p in patients:  # iteration/loop requirement
        queue_list.insert('', 'end', values=(p['Time'], p['Name'], p['Age'], p['Priority'], p['Status']))


def add_patient():
    """Button function - combines GUI + backend logic"""
    name = entry_name.get()
    age = entry_age.get()
    complaint = entry_complaint.get()

    priority = calculate_priority(age, complaint)  # call function

    if save_patient(name, age, complaint, priority):
        messagebox.showinfo("Success", f"Patient {name} added with {priority} priority")
        clear_fields()
        refresh_queue()


def clear_fields():
    """Clear button function"""
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_complaint.delete(0, tk.END)


def exit_app():
    """Exit button function"""
    root.destroy()


# === GUI DESIGN - tkinter required ===
root = tk.Tk()
root.title("Freetown Community Clinic - Queue System")
root.geometry("700x500")
root.resizable(False, False)

# Labels + Entry fields
frame_input = tk.Frame(root, padx=10, pady=10)
frame_input.pack(fill='x')

tk.Label(frame_input, text="Patient Name:").grid(row=0, column=0, sticky='w', pady=5)
entry_name = tk.Entry(frame_input, width=40)
entry_name.grid(row=0, column=1, pady=5)

tk.Label(frame_input, text="Age:").grid(row=1, column=0, sticky='w', pady=5)
entry_age = tk.Entry(frame_input, width=10)
entry_age.grid(row=1, column=1, sticky='w', pady=5)

tk.Label(frame_input, text="Complaint:").grid(row=2, column=0, sticky='w', pady=5)
entry_complaint = tk.Entry(frame_input, width=40)
entry_complaint.grid(row=2, column=1, pady=5)

# Buttons: Calculate=Add, Clear, Exit
frame_buttons = tk.Frame(root, pady=10)
frame_buttons.pack()

tk.Button(frame_buttons, text="Add Patient", command=add_patient, bg="#4CAF50", fg="white", width=15).grid(row=0,
                                                                                                           column=0,
                                                                                                           padx=5)
tk.Button(frame_buttons, text="Clear", command=clear_fields, width=15).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Exit", command=exit_app, bg="#f44336", fg="white", width=15).grid(row=0, column=2,
                                                                                                 padx=5)

# Output display area - Table format
frame_output = tk.Frame(root, padx=10, pady=10)
frame_output.pack(fill='both', expand=True)

tk.Label(frame_output, text="Current Queue:", font=("Tahoma", 10, "bold")).pack(anchor='w')

columns = ('Time', 'Name', 'Age', 'Priority', 'Status')
queue_list = ttk.Treeview(frame_output, columns=columns, show='headings')
for col in columns:
    queue_list.heading(col, text=col)
    queue_list.column(col, width=120)
queue_list.pack(fill='both', expand=True)

# Load data on startup
refresh_queue()

root.mainloop()