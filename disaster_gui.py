import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vaishu!TheGr8",
        database="disaster"
    )

conn = get_connection()
print("DB Connected")

root = tk.Tk()
root.title("Disaster Relief Management System")
root.geometry("1100x650")
style = ttk.Style()
style.theme_use('clam')

style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 10))

tab_control = ttk.Notebook(root)

pastel_green = "#d2f5d2"
pastel_blue = "#d2e9f5"
pastel_purple = "#e6d2f5" 
pastel_yellow = "#f5f2d2"
tab_control = ttk.Notebook(root)
tab_control.pack(fill='both', expand=True)

pastel_green = "#d2f5d2"
pastel_blue = "#d2e9f5"
pastel_purple = "#e6d2f5" 
pastel_yellow = "#f5f2d2"


# Victim Tab
victim_tab = tk.Frame(tab_control, bg=pastel_green)
tab_control.add(victim_tab, text='Victims')

# Victim fields
fields = [
    ("Victim ID", 0), ("Name", 1), ("Age", 2),
    ("Address", 3), ("Relief Centre ID", 4), ("Disaster ID", 5)
]
entries = {}

for label_text, row in fields:
    tk.Label(victim_tab, text=label_text, bg=pastel_green).grid(row=row, column=0, padx=10, pady=5, sticky='w')
    entry = ttk.Entry(victim_tab)
    entry.grid(row=row, column=1, padx=10, pady=5)
    entries[label_text] = entry

# Search fields
search_fields = [
    ("Search by Victim ID", 6), ("Search by Disaster ID", 7), ("Search by Relief Centre ID", 8)
]
search_entries = {}

for label_text, row in search_fields:
    tk.Label(victim_tab, text=label_text, bg=pastel_green).grid(row=row, column=0, padx=10, pady=5, sticky='w')
    search_entry = ttk.Entry(victim_tab)
    search_entry.grid(row=row, column=1, padx=10, pady=5)
    search_entries[label_text] = search_entry

# Treeview to display victim data
victim_tree = ttk.Treeview(
    victim_tab,
    columns=("VictimID", "DisasterID", "VictimName", "Age", "Address", "ReliefCentreID", ),
    show='headings'
)

columns = [
    ("VictimID", 120),
    ("DisasterID", 120), 
    ("VictimName", 180),
    ("Age", 120),
    ("Address", 180),
    ("ReliefCentreID", 120),
]

for col, width in columns:
    victim_tree.heading(col, text=col)
    victim_tree.column(col, width=width, anchor=tk.CENTER)

# Positioning Treeview on the victim_tab
victim_tree.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Load Victims Function (searches by any or all filters)
def load_victims():
    victim_id = search_entries["Search by Victim ID"].get().strip()
    disaster_id = search_entries["Search by Disaster ID"].get().strip()
    relief_centre_id = search_entries["Search by Relief Centre ID"].get().strip()

    query = "SELECT * FROM victim WHERE 1=1"
    params = []

    if victim_id:
        query += " AND victim_id = %s"
        params.append(victim_id)
    if disaster_id:
        query += " AND disaster_id LIKE %s"
        params.append(f"%{disaster_id}%")
    if relief_centre_id:
        query += " AND reliefcentre_id LIKE %s"
        params.append(f"%{relief_centre_id}%")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        for item in victim_tree.get_children():
            victim_tree.delete(item)

        for row in rows:
            victim_tree.insert("", tk.END, values=row)

    except Exception as e:
        messagebox.showerror("Error", f"Could not load data: {e}")


def on_victim_select(event):
    selected_item = victim_tree.selection()
    if not selected_item:
        return
    values = victim_tree.item(selected_item, 'values')
    entries["Victim ID"].delete(0, tk.END)
    entries["Victim ID"].insert(0, values[0])
    entries["Disaster ID"].delete(0, tk.END)
    entries["Disaster ID"].insert(0, values[1])
    entries["Name"].delete(0, tk.END)
    entries["Name"].insert(0, values[2])
    entries["Age"].delete(0, tk.END)
    entries["Age"].insert(0, values[3])
    entries["Address"].delete(0, tk.END)
    entries["Address"].insert(0, values[4])
    entries["Relief Centre ID"].delete(0, tk.END)
    entries["Relief Centre ID"].insert(0, values[5])


# Register Victim Function
def register_victim():
    try:
        data = {key: entry.get().strip() for key, entry in entries.items()}
        age = int(data["Age"])

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(""" 
            INSERT INTO victim (victim_id, victim_name, age, address, reliefcentre_id, disaster_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data["Victim ID"], data["Name"], age,
            data["Address"], data["Relief Centre ID"], data["Disaster ID"]
        ))

        if age < 18:
            cursor.execute("INSERT INTO minor_victim (victim_name, age) VALUES (%s, %s)", (data["Name"], age))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Victim registered successfully.")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid numeric age.")
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
ttk.Button(victim_tab, text="Register Victim", command=register_victim).grid(row=10, column=1, pady=10)
ttk.Button(victim_tab, text="Load Victim Data", command=load_victims).grid(row=11, column=1, pady=5)

# Delete Victim Function
def delete_victim():
    selected_item = victim_tree.selection()
    if not selected_item:
        messagebox.showwarning("Select Victim", "Please select a victim to delete.")
        return

    item_values = victim_tree.item(selected_item, 'values')
    victim_id = item_values[0]
    disaster_id = item_values[1]

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Victim ID: {victim_id} (Disaster: {disaster_id})?")
    if not confirm:
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM victim WHERE victim_id = %s AND disaster_id = %s", (victim_id, disaster_id))
        conn.commit()
        conn.close()
        load_victims()
        messagebox.showinfo("Success", "Victim deleted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not delete victim: {e}")
ttk.Button(victim_tab, text="Delete Selected Victim", command=delete_victim).grid(row=12, column=1, pady=5)

# Update Victim Function
def update_victim():
    selected_item = victim_tree.selection()
    if not selected_item:
        messagebox.showwarning("Select Victim", "Please select a victim to update.")
        return

    item_values = victim_tree.item(selected_item, 'values')
    old_victim_id = item_values[0]
    old_disaster_id = item_values[1]

    # Safely retrieve new values from entries
    new_victim_id = entries["Victim ID"].get().strip()
    name = entries["Name"].get().strip()
    age_str = entries["Age"].get().strip()
    address = entries["Address"].get().strip()
    relief = entries["Relief Centre ID"].get().strip()
    new_disaster_id = entries["Disaster ID"].get().strip()

    if not new_victim_id or not name or not age_str or not address or not relief or not new_disaster_id:
        messagebox.showerror("Input Error", "All fields must be filled.")
        return

    try:
        age = int(age_str)
    except ValueError:
        messagebox.showerror("Invalid Input", "Age must be a valid number.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE victim 
            SET victim_id = %s, victim_name = %s, age = %s, address = %s, reliefcentre_id = %s, disaster_id = %s 
            WHERE victim_id = %s AND disaster_id = %s
        """, (
            new_victim_id, name, age, address, relief, new_disaster_id,
            old_victim_id, old_disaster_id
        ))

        conn.commit()
        conn.close()
        load_victims()
        messagebox.showinfo("Success", "Victim updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not update victim:\n{e}")

ttk.Button(victim_tab, text="Update Selected Victim", command=update_victim).grid(row=13, column=1, pady=5)
victim_tree.bind("<<TreeviewSelect>>", on_victim_select)




# Volunteer Tab
volunteer_tab = tk.Frame(tab_control, bg=pastel_blue)
tab_control.add(volunteer_tab, text='Volunteers')

tk.Label(volunteer_tab, text="Volunteer ID", bg=pastel_blue).grid(row=0, column=0, padx=10, pady=5, sticky='w')
vol_id = ttk.Entry(volunteer_tab)
vol_id.grid(row=0, column=1)

tk.Label(volunteer_tab, text="Name", bg=pastel_blue).grid(row=1, column=0, padx=10, pady=5, sticky='w')
vol_name = ttk.Entry(volunteer_tab)
vol_name.grid(row=1, column=1)

tk.Label(volunteer_tab, text="Age", bg=pastel_blue).grid(row=2, column=0, padx=10, pady=5, sticky='w')
vol_age = ttk.Entry(volunteer_tab)
vol_age.grid(row=2, column=1)

tk.Label(volunteer_tab, text="Relief Centre ID", bg=pastel_blue).grid(row=3, column=0, padx=10, pady=5, sticky='w')
vol_relief = ttk.Entry(volunteer_tab)
vol_relief.grid(row=3, column=1)

tk.Label(volunteer_tab, text="Disaster ID", bg=pastel_blue).grid(row=4, column=0, padx=10, pady=5, sticky='w')
vol_disaster = ttk.Entry(volunteer_tab)
vol_disaster.grid(row=4, column=1)

def register_volunteer():
    try:
        volunteer_id = vol_id.get().strip()
        name = vol_name.get().strip()
        age = int(vol_age.get().strip())
        relief = vol_relief.get().strip()
        disaster_id = vol_disaster.get().strip()

        if not volunteer_id or not name or not relief or not disaster_id:
            messagebox.showerror("Input Error", "All fields must be filled.")
            return

        if age < 18:
            messagebox.showerror("Age Restriction", "Volunteers must be at least 18 years old.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO volunteer (volunteer_id, name, age, reliefcentre_id, disaster_id) VALUES (%s, %s, %s, %s, %s)",
            (volunteer_id, name, age, relief, disaster_id)
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Volunteer registered successfully.")
        load_volunteers()
    except ValueError:
        messagebox.showerror("Invalid Input", "Age must be a number.")
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

ttk.Button(volunteer_tab, text="Register Volunteer", command=register_volunteer).grid(row=5, column=1, pady=10)

# --- Search Section ---
tk.Label(volunteer_tab, text="Search by Volunteer ID", bg=pastel_blue).grid(row=6, column=0, padx=10, pady=5, sticky='w')
search_vol_id = ttk.Entry(volunteer_tab)
search_vol_id.grid(row=6, column=1)

tk.Label(volunteer_tab, text="Search by Disaster ID", bg=pastel_blue).grid(row=7, column=0, padx=10, pady=5, sticky='w')
search_disaster_id = ttk.Entry(volunteer_tab)
search_disaster_id.grid(row=7, column=1)

tk.Label(volunteer_tab, text="Search by Relief Centre ID", bg=pastel_blue).grid(row=8, column=0, padx=10, pady=5, sticky='w')
search_relief_id = ttk.Entry(volunteer_tab)
search_relief_id.grid(row=8, column=1)

vol_tree = ttk.Treeview(volunteer_tab, columns=("ID", "Name", "Age", "DisasterID", "ReliefCentre"), show='headings')
vol_tree.heading("ID", text="Volunteer ID")
vol_tree.heading("Name", text="Name")
vol_tree.heading("Age", text="Age")
vol_tree.heading("DisasterID", text="Disaster ID")
vol_tree.heading("ReliefCentre", text="Relief Centre ID")
vol_tree.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

def load_volunteers():
    vol_id_val = search_vol_id.get().strip()
    disaster_val = search_disaster_id.get().strip()
    relief_val = search_relief_id.get().strip()

    query = "SELECT * FROM volunteer WHERE 1=1"
    params = []

    if vol_id_val:
        query += " AND volunteer_id LIKE %s"
        params.append(f"%{vol_id_val}%")
    if disaster_val:
        query += " AND disaster_id LIKE %s"
        params.append(f"%{disaster_val}%")
    if relief_val:
        query += " AND reliefcentre_id LIKE %s"
        params.append(f"%{relief_val}%")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        for item in vol_tree.get_children():
            vol_tree.delete(item)

        for row in rows:
            vol_tree.insert("", tk.END, values=row)

    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch data: {e}")

ttk.Button(volunteer_tab, text="Search Volunteers", command=load_volunteers).grid(row=9, column=1, pady=10)

# --- Delete Feature ---
def delete_volunteer():
    selected_item = vol_tree.selection()
    if not selected_item:
        messagebox.showwarning("Select Volunteer", "Please select a volunteer to delete.")
        return

    item_values = vol_tree.item(selected_item, 'values')
    volunteer_id = item_values[0]
    disaster_id = item_values[3]  # Assuming Disaster ID is the 4th column (index 3)

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Volunteer ID: {volunteer_id} (Disaster: {disaster_id})?")
    if not confirm:
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM volunteer WHERE volunteer_id = %s AND disaster_id = %s", (volunteer_id, disaster_id))
        conn.commit()
        conn.close()
        load_volunteers()
        messagebox.showinfo("Success", "Volunteer deleted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not delete volunteer: {e}")

# Button to delete volunteer
ttk.Button(volunteer_tab, text="Delete Selected Volunteer", command=delete_volunteer).grid(row=11, column=1, pady=5)

# --- Update Feature ---
def populate_form_from_tree(event=None):
    selected = vol_tree.selection()
    if selected:
        item = vol_tree.item(selected[0])
        vals = item["values"]
        vol_id.delete(0, tk.END)
        vol_id.insert(0, vals[0])
        vol_name.delete(0, tk.END)
        vol_name.insert(0, vals[1])
        vol_age.delete(0, tk.END)
        vol_age.insert(0, vals[2])
        vol_disaster.delete(0, tk.END)
        vol_disaster.insert(0, vals[3])
        vol_relief.delete(0, tk.END)
        vol_relief.insert(0, vals[4])

vol_tree.bind("<<TreeviewSelect>>", populate_form_from_tree)

def update_volunteer():
    selected_item = vol_tree.selection()
    if not selected_item:
        messagebox.showwarning("Select Volunteer", "Please select a volunteer to update.")
        return

    # Get current values from the selected row
    item_values = vol_tree.item(selected_item, 'values')
    old_volunteer_id = item_values[0]
    old_disaster_id = item_values[3]  # Index 3 is Disaster ID in Treeview

    # Get new values from the entry fields
    new_volunteer_id = vol_id.get().strip()
    name = vol_name.get().strip()
    try:
        age = int(vol_age.get().strip())
    except ValueError:
        messagebox.showerror("Invalid Input", "Age must be a number.")
        return

    relief = vol_relief.get().strip()
    new_disaster_id = vol_disaster.get().strip()

    if not new_volunteer_id or not name or not relief or not new_disaster_id:
        messagebox.showerror("Input Error", "All fields must be filled.")
        return

    if age < 18:
        messagebox.showerror("Age Restriction", "Volunteers must be at least 18 years old.")
        return

    confirm = messagebox.askyesno("Confirm Update", f"Are you sure you want to update Volunteer ID: {old_volunteer_id}?")
    if not confirm:
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Use old keys in WHERE clause to find the correct record
        update_query = """
            UPDATE volunteer 
            SET volunteer_id = %s, name = %s, age = %s, reliefcentre_id = %s, disaster_id = %s 
            WHERE volunteer_id = %s AND disaster_id = %s
        """
        cursor.execute(update_query, (
            new_volunteer_id, name, age, relief, new_disaster_id,
            old_volunteer_id, old_disaster_id
        ))

        conn.commit()
        conn.close()
        load_volunteers()
        messagebox.showinfo("Success", "Volunteer updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not update volunteer: {e}")
ttk.Button(volunteer_tab, text="Update Volunteer", command=update_volunteer).grid(row=12, column=1, pady=5)



# Medical Assistance Tab
medical_tab = tk.Frame(tab_control, bg=pastel_yellow)
tab_control.add(medical_tab, text='Medical Assistance')

# Labels and Entries
medical_labels = ["Hospital ID", "Victim ID", "Treatment", "Date Treated"]
medical_entries = {}

for idx, label in enumerate(medical_labels):
    tk.Label(medical_tab, text=label, bg=pastel_yellow).grid(row=idx, column=0, padx=10, pady=5, sticky='w')
    entry = ttk.Entry(medical_tab)
    entry.grid(row=idx, column=1, padx=10, pady=5)
    medical_entries[label] = entry

def submit_medical():
    hospitalid = medical_entries["Hospital ID"].get()
    victim_id = medical_entries["Victim ID"].get()
    treatment = medical_entries["Treatment"].get()
    date_treated = medical_entries["Date Treated"].get()

    if not hospitalid or not victim_id or not treatment or not date_treated:
        messagebox.showerror("Input Error", "All fields must be filled.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO medical_assistance (hospitalid, victim_id, treatment, date_treated)
            VALUES (%s, %s, %s, %s)
        """, (hospitalid, victim_id, treatment, date_treated))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Medical assistance record added.")
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

ttk.Button(medical_tab, text="Submit Assistance", command=submit_medical).grid(row=4, column=1, pady=10)

# --- Search Section ---
tk.Label(medical_tab, text="Search by Hospital ID", bg=pastel_yellow).grid(row=5, column=0, padx=10, pady=5, sticky='w')
search_hospital = ttk.Entry(medical_tab)
search_hospital.grid(row=5, column=1)

tk.Label(medical_tab, text="Search by Victim ID", bg=pastel_yellow).grid(row=6, column=0, padx=10, pady=5, sticky='w')
search_victim = ttk.Entry(medical_tab)
search_victim.grid(row=6, column=1)

# Treeview to display results
medical_tree = ttk.Treeview(medical_tab, columns=("HospitalID", "VictimID", "Treatment", "DateTreated"), show='headings')
medical_tree.heading("HospitalID", text="Hospital ID")
medical_tree.heading("VictimID", text="Victim ID")
medical_tree.heading("Treatment", text="Treatment")
medical_tree.heading("DateTreated", text="Date Treated")
medical_tree.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

def on_medical_select(event):
    selected = medical_tree.selection()
    if not selected:
        return
    values = medical_tree.item(selected[0], 'values')
    medical_entries["Hospital ID"].delete(0, tk.END)
    medical_entries["Hospital ID"].insert(0, values[0])
    medical_entries["Victim ID"].delete(0, tk.END)
    medical_entries["Victim ID"].insert(0, values[1])
    medical_entries["Treatment"].delete(0, tk.END)
    medical_entries["Treatment"].insert(0, values[2])
    medical_entries["Date Treated"].delete(0, tk.END)
    medical_entries["Date Treated"].insert(0, values[3])

def load_medical_assistance():
    hospital_val = search_hospital.get().strip()
    victim_val = search_victim.get().strip()

    query = "SELECT * FROM medical_assistance WHERE 1=1"
    params = []

    if hospital_val:
        query += " AND hospitalid LIKE %s"
        params.append(f"%{hospital_val}%")
    if victim_val:
        query += " AND victim_id LIKE %s"
        params.append(f"%{victim_val}%")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        # Clear old data
        for item in medical_tree.get_children():
            medical_tree.delete(item)

        # Insert new data into the Treeview
        for row in rows:
            medical_tree.insert("", tk.END, values=row)

    except Exception as e:
        messagebox.showerror("Error", f"Search failed: {e}")

ttk.Button(medical_tab, text="Search Assistance", command=load_medical_assistance).grid(row=7, column=1, pady=10)

# --- Delete Button ---
def delete_selected_assistance():
    selected = medical_tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a record to delete.")
        return

    item = medical_tree.item(selected[0])
    hospitalid = item["values"][0]

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Hospital ID {hospitalid}?")
    if confirm:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM medical_assistance WHERE hospitalid = %s", (hospitalid,))
            conn.commit()
            conn.close()
            medical_tree.delete(selected[0])
            messagebox.showinfo("Deleted", f"Hospital ID {hospitalid} deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete: {e}")

ttk.Button(medical_tab, text="Delete Selected Assistance", command=delete_selected_assistance).grid(row=9, column=1, pady=5)

# --- Update Button ---
def update_selected_assistance():
    selected = medical_tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a record to update.")
        return

    old_hospitalid = medical_tree.item(selected[0], 'values')[0]
    old_victim_id = medical_tree.item(selected[0], 'values')[1]

    new_hospitalid = medical_entries["Hospital ID"].get().strip()
    victim_id = medical_entries["Victim ID"].get().strip()
    treatment = medical_entries["Treatment"].get().strip()
    date_treated = medical_entries["Date Treated"].get().strip()

    if not new_hospitalid or not victim_id or not treatment or not date_treated:
        messagebox.showerror("Input Error", "All fields must be filled to update.")
        return

    # Check if the victim_id is changing
    if victim_id != old_victim_id:
        messagebox.showerror("Input Error", "The victim ID cannot be changed. It is unique.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if the new hospitalid already exists
        cursor.execute("SELECT COUNT(*) FROM medical_assistance WHERE hospitalID = %s", (new_hospitalid,))
        count = cursor.fetchone()[0]

        if count > 0 and new_hospitalid != old_hospitalid:
            messagebox.showerror("Duplicate Error", "The new Hospital ID already exists.")
            conn.close()
            return

        # Execute the UPDATE query
        cursor.execute("""
            UPDATE medical_assistance 
            SET hospitalID = %s, victim_id = %s, treatment = %s, date_treated = %s 
            WHERE hospitalID = %s
        """, (new_hospitalid, victim_id, treatment, date_treated, old_hospitalid))

        conn.commit()
        conn.close()
        load_medical_assistance()  # Refresh the Treeview
        messagebox.showinfo("Success", "Medical assistance record updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Update failed: {e}")


ttk.Button(medical_tab, text="Update Selected Assistance", command=update_selected_assistance).grid(row=10, column=1, pady=5)

medical_tree.bind("<<TreeviewSelect>>", on_medical_select)


# Evacuation Plan Tab
evac_tab = tk.Frame(tab_control, bg=pastel_purple)
tab_control.add(evac_tab, text='Evacuation Plans')

evac_labels = ["Plan ID", "Disaster ID", "Relief Centre ID"]
evac_entries = {}

for idx, label in enumerate(evac_labels):
    tk.Label(evac_tab, text=label, bg=pastel_purple).grid(row=idx, column=0, padx=10, pady=5, sticky='w')
    entry = ttk.Entry(evac_tab)
    entry.grid(row=idx, column=1, padx=10, pady=5)
    evac_entries[label] = entry

def submit_evac():
    planid = evac_entries["Plan ID"].get()
    disaster = evac_entries["Disaster ID"].get()
    relief = evac_entries["Relief Centre ID"].get()
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO evacuationplan (planid, disaster_id, reliefcentre_id) VALUES (%s, %s, %s)",
                       (planid, disaster, relief))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Evacuation plan added.")
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

ttk.Button(evac_tab, text="Submit Plan", command=submit_evac).grid(row=3, column=1, pady=10)

# --- Search Section ---
tk.Label(evac_tab, text="Search by Plan ID", bg=pastel_purple).grid(row=4, column=0, padx=10, pady=5, sticky='w')
search_plan = ttk.Entry(evac_tab)
search_plan.grid(row=4, column=1)

tk.Label(evac_tab, text="Search by Disaster ID", bg=pastel_purple).grid(row=5, column=0, padx=10, pady=5, sticky='w')
search_disaster = ttk.Entry(evac_tab)
search_disaster.grid(row=5, column=1)

tk.Label(evac_tab, text="Search by Relief Centre ID", bg=pastel_purple).grid(row=6, column=0, padx=10, pady=5, sticky='w')
search_relief = ttk.Entry(evac_tab)
search_relief.grid(row=6, column=1)

# Treeview to display results
evac_tree = ttk.Treeview(evac_tab, columns=("PlanID", "ReliefCentreID", "DisasterID"), show='headings')
evac_tree.heading("PlanID", text="Plan ID")
evac_tree.heading("ReliefCentreID", text="Relief Centre ID")
evac_tree.heading("DisasterID", text="Disaster ID")
evac_tree.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

def on_evac_select(event):
    selected = evac_tree.selection()
    if not selected:
        return
    values = evac_tree.item(selected[0], 'values')
    evac_entries["Plan ID"].delete(0, tk.END)
    evac_entries["Plan ID"].insert(0, values[0])
    evac_entries["Relief Centre ID"].delete(0, tk.END)
    evac_entries["Relief Centre ID"].insert(0, values[1])
    evac_entries["Disaster ID"].delete(0, tk.END)
    evac_entries["Disaster ID"].insert(0, values[2])


def load_evacuation_plans():
    plan_val = search_plan.get().strip()
    disaster_val = search_disaster.get().strip()
    relief_val = search_relief.get().strip()

    query = "SELECT * FROM evacuationplan WHERE 1=1"
    params = []

    if plan_val:
        query += " AND planid LIKE %s"
        params.append(f"%{plan_val}%")
    if disaster_val:
        query += " AND disaster_id LIKE %s"
        params.append(f"%{disaster_val}%")
    if relief_val:
        query += " AND reliefcentre_id LIKE %s"
        params.append(f"%{relief_val}%")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        # Clear old data
        for item in evac_tree.get_children():
            evac_tree.delete(item)

        for row in rows:
            evac_tree.insert("", tk.END, values=row)

    except Exception as e:
        messagebox.showerror("Error", f"Search failed: {e}")

ttk.Button(evac_tab, text="Search Plans", command=load_evacuation_plans).grid(row=7, column=1, pady=10)

# --- Delete Button ---
def delete_selected_plan():
    selected = evac_tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a plan to delete.")
        return

    item = evac_tree.item(selected[0])
    planid = item["values"][0]

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Plan ID {planid}?")
    if confirm:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM evacuationplan WHERE planid = %s", (planid,))
            conn.commit()
            conn.close()
            evac_tree.delete(selected[0])
            messagebox.showinfo("Deleted", f"Plan ID {planid} deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete: {e}")

ttk.Button(evac_tab, text="Delete Selected Plan", command=delete_selected_plan).grid(row=9, column=1, pady=5)

def update_selected_plan():
    selected = evac_tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a plan to update.")
        return

    old_plan_id = evac_tree.item(selected[0], 'values')[0]

    new_plan_id = evac_entries["Plan ID"].get().strip()
    disaster_id = evac_entries["Disaster ID"].get().strip()
    reliefcentre_id = evac_entries["Relief Centre ID"].get().strip()

    if not new_plan_id or not disaster_id or not reliefcentre_id:
        messagebox.showerror("Input Error", "All fields must be filled to update.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE evacuationplan 
            SET planid = %s, disaster_id = %s, reliefcentre_id = %s 
            WHERE planid = %s
        """, (new_plan_id, disaster_id, reliefcentre_id, old_plan_id))
        conn.commit()
        conn.close()
        load_evacuation_plans()
        messagebox.showinfo("Success", "Evacuation plan updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Update failed: {e}")
ttk.Button(evac_tab, text="Update Selected Plan", command=update_selected_plan).grid(row=10, column=1, pady=5)
evac_tree.bind("<<TreeviewSelect>>", on_evac_select)


# Evacuation Routes Tab
routes_tab = tk.Frame(tab_control, bg="#f5e2d2")
tab_control.add(routes_tab, text='Evacuation Routes')

# --- Input Fields ---
tk.Label(routes_tab, text="Plan ID", bg="#f5e2d2").grid(row=0, column=0, padx=10, pady=5, sticky='w')
route_plan_id = ttk.Entry(routes_tab)
route_plan_id.grid(row=0, column=1)

tk.Label(routes_tab, text="Evacuation Route", bg="#f5e2d2").grid(row=1, column=0, padx=10, pady=5, sticky='w')
route_text = ttk.Entry(routes_tab)
route_text.grid(row=1, column=1)

def add_route():
    planid = route_plan_id.get()
    route = route_text.get()
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO evacuation_routes (planid, route) VALUES (%s, %s)", (planid, route))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Evacuation route added.")
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

ttk.Button(routes_tab, text="Add Route", command=add_route).grid(row=2, column=1, pady=10)

# --- Search Section ---
tk.Label(routes_tab, text="Search by Plan ID", bg="#f5e2d2").grid(row=3, column=0, padx=10, pady=5, sticky='w')
search_planid = ttk.Entry(routes_tab)
search_planid.grid(row=3, column=1)

# Treeview to show search results
routes_tree = ttk.Treeview(routes_tab, columns=("PlanID", "Route"), show='headings')
routes_tree.heading("PlanID", text="Plan ID")
routes_tree.heading("Route", text="Evacuation Route")
routes_tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

def on_route_select(event):
    selected_item = routes_tree.selection()
    if not selected_item:
        return
    values = routes_tree.item(selected_item, 'values')
    route_plan_id.delete(0, tk.END)
    route_plan_id.insert(0, values[0])
    route_text.delete(0, tk.END)
    route_text.insert(0, values[1])


def search_routes():
    plan_id = search_planid.get().strip()

    query = "SELECT * FROM evacuation_routes WHERE 1=1"
    params = []
    if plan_id:
        query += " AND planid LIKE %s"
        params.append(f"%{plan_id}%")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        # Clear existing results
        for row in routes_tree.get_children():
            routes_tree.delete(row)

        for row in rows:
            routes_tree.insert("", tk.END, values=row)

    except Exception as e:
        messagebox.showerror("Error", f"Search failed: {e}")

ttk.Button(routes_tab, text="Search", command=search_routes).grid(row=4, column=1, pady=5)

def load_routes():
    plan_id = search_planid.get().strip()

    query = "SELECT * FROM evacuation_routes WHERE 1=1"
    params = []
    if plan_id:
        query += " AND planid LIKE %s"
        params.append(f"%{plan_id}%")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        # Clear old data
        for row in routes_tree.get_children():
            routes_tree.delete(row)

        for row in rows:
            routes_tree.insert("", tk.END, values=row)

    except Exception as e:
        messagebox.showerror("Error", f"Search failed: {e}")


# --- Delete Selected Route ---
def delete_selected_route():
    selected_item = routes_tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a route to delete.")
        return

    values = routes_tree.item(selected_item)["values"]
    planid = values[0]

    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Plan ID '{planid}'?")
    if confirm:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM evacuation_routes WHERE planid = %s", (planid,))
            conn.commit()
            conn.close()

            routes_tree.delete(selected_item)
            messagebox.showinfo("Deleted", f"Plan ID '{planid}' deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Deletion failed: {e}")
ttk.Button(routes_tab, text="Delete Selected Route", command=delete_selected_route).grid(row=6, column=1, pady=5)

def update_route():
    selected_item = routes_tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a route to update.")
        return

    old_planid = routes_tree.item(selected_item)["values"][0]

    new_planid = route_plan_id.get().strip()
    new_route = route_text.get().strip()

    if not new_planid or not new_route:
        messagebox.showerror("Input Error", "Both fields must be filled to update.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE evacuation_routes 
            SET planid = %s, route = %s 
            WHERE planid = %s
        """, (new_planid, new_route, old_planid))
        conn.commit()
        conn.close()

        load_routes()  # Re-load routes to reflect changes
        messagebox.showinfo("Success", "Evacuation route updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Update failed: {e}")
ttk.Button(routes_tab, text="Update Selected Route", command=update_route).grid(row=7, column=1, pady=5)

routes_tree.bind("<<TreeviewSelect>>", on_route_select)


tab_control.pack(expand=1, fill='both')
root.mainloop()
