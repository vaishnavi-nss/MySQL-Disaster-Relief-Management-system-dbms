# MySQL-Disaster-Relief-Management-system-dbms

A database-driven application designed to efficiently manage disaster-related data including victims, volunteers, relief centers, and evacuation plans. Built using MySQL and Python (Tkinter GUI), the system streamlines data entry, search, reporting, and disaster-wise tracking of affected individuals.

---

## 📌 Table of Contents

* [About the Project](#about-the-project)
* [Key Features](#key-features)
* [Database Design](#database-design)
* [Tech Stack](#tech-stack)
* [How to Run](#how-to-run)
* [Screenshots](#screenshots)
* [Future Enhancements](#future-enhancements)
* [License](#license)

---

## 📖 About the Project

During disasters, effective coordination between relief centers, medical responders, and authorities is essential. This project provides a structured way to:

* Track affected **victims**
* Assign **volunteers** efficiently
* Manage **relief centers**
* Monitor **evacuation routes** and disaster-specific records

It uses **MySQL** for structured data storage and **Python Tkinter GUI** for user-friendly interaction.

---

## 🌟 Key Features

* Add/view/update/delete **victim**, **volunteer**, **medical_assistance**,  **evacauation_plans** and **evacauation_routes** details
* Assign victims to **relief centres**
* Record **medical conditions** and **spoken languages** of victims
* Flag **vulnerable individuals** (e.g., minors or elderly)
* Track **volunteer eligibility** (age > 18)
* Integrated search and **disaster-wise filtering**
* Real-time **victim/volunteer counts per disaster**
* Automated logs using SQL **triggers** (insert/update/delete)

---

## 🗂️ Database Design

**Main Tables:**

* `victim(victim_id, name, age, address, disaster_id, reliefcentre_id)`
* `volunteer(volunteer_id, name, age, disaster_id)`
* `disaster(disaster_id, name, helpline)`
* `relief_centre(centre_id, location)`
* `medical_condition(victim_id, condition)`
* `languages(victim_id, language)`

**Advanced Features:**

* SQL **views** for vulnerability tracking
* **AFTER triggers** for insert/update/delete logging
* **Stored procedures/cursors** for batch operations

---

## 🛠 Tech Stack

| Layer     | Technology               |
| --------- | ------------------------ |
| Frontend  | Python Tkinter GUI       |
| Backend   | MySQL                    |
| Scripting | Python (mysql-connector) |
| DB Tools  | MySQL Workbench          |

---

## ▶️ How to Run

1. Clone the repo:

   ```bash
   git clone [https://github.com/yourusername/disaster-management-dbms.git](https://github.com/vaishnavi-nss/MySQL-Disaster-Relief-Management-system-dbms)
   cd disaster-management-dbms
   ```
2. Import the SQL schema in MySQL Workbench.
3. Update your DB credentials in `config.py`.
4. Run the GUI:

   ```bash
   python app.py
   ```

---

## 🖼️ Screenshots

Victim Tab with operations

![image](https://github.com/user-attachments/assets/ca208e91-018b-4167-b264-3d3dac7a1830)
![image](https://github.com/user-attachments/assets/ef941cfd-d46f-47b1-ae56-112632f9e7d7)
![image](https://github.com/user-attachments/assets/505d2d05-21ec-48d3-b138-de62cee8ccf4)
![image](https://github.com/user-attachments/assets/217241c1-fc22-47e4-8d4e-a6322a079727)
![image](https://github.com/user-attachments/assets/b21c3dc3-417e-4873-bf33-b613eed4ddca)

Volunteer Tab

![image](https://github.com/user-attachments/assets/d5506e3b-0136-4c0e-9a15-8d52a41e03f4)

Medical Assistance Tab

![image](https://github.com/user-attachments/assets/6dbfbb79-e5e3-49e8-a91e-3ec15593732d)

Evacuation Plan

![image](https://github.com/user-attachments/assets/f4610a38-4631-4abd-9ff2-81f475a193cf)

Evacuation Routes

![image](https://github.com/user-attachments/assets/237f265b-6903-41c7-be45-9c3c66812971)

---

## 🚀 Future Enhancements

* Web-based interface using Flask or Django
* Role-based access (admin vs volunteer)
* SMS/Email notifications to victims and volunteers
* Geo-mapping for relief center visualization
* Disaster severity prediction using ML

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgements

* DBMS concepts from academic curriculum
* MySQL official docs
* Tkinter community tutorials

---
