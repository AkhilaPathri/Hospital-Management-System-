# 🏥 Professional Hospital Management System

A modern, web-based Hospital Management System developed with **Python** and **Streamlit**. This application streamlines hospital operations, from patient management to billing and analytics, with a beautiful and professional user interface.

---

## 🚀 Features

- **User Authentication** (Admin, Doctor, Nurse, Creator)
- **Patient Management**
  - Add, edit, and view patient records
  - Track admissions & discharges
  - Medical history, allergies, and more
- **Doctor Management**
  - Add and manage doctor profiles
  - Specializations, experience, schedules
- **Appointment Scheduling**
  - Easy patient-doctor appointment booking
  - Calendar and list views
  - Status tracking (Scheduled, Completed, etc.)
- **Billing & Financial Management**
  - Generate bills with itemized charges
  - Track payments and revenue analytics
- **Inventory Management**
  - Medicines & equipment tracking
  - Low-stock alerts
- **Comprehensive Dashboard & Reports**
  - Quick stats
  - Data visualization (Pie, Bar charts)
- **Professional UI/UX**
  - Custom CSS and modern layouts
  - Responsive and user-friendly

---

## 🖥️ Screenshots

<!-- You can add screenshots here by uploading images to the repo and using: -->
<!-- ![Screenshot](screenshots/dashboard.png) -->

---

## 📝 Getting Started

### 1. **Clone the Repository**

```bash
git clone https://github.com/YOUR_USERNAME/hospital-management-system.git
cd hospital-management-system
```

### 2. **Install Requirements**

```bash
pip install -r requirements.txt
```

**Required libraries:**

- streamlit
- pandas
- plotly

*If there's no `requirements.txt`, create one:*

```txt name=requirements.txt
streamlit
pandas
plotly
```

### 3. **Run the Application**

```bash
streamlit run app.py
```

The app will open in your browser.  
Login using the demo credentials provided below.

---

## 👤 Demo Credentials

| Role         | Username | Password     |
| ------------ | -------- | ------------ |
| Administrator| admin    | admin123     |
| Doctor       | doctor   | doc123       |
| Nurse        | nurse    | nurse123     |
| Creator      | akhila   | mypassword   |

---

## 📂 Project Structure

```
hospital-management-system/
├── app.py
├── data/
│   ├── patients.json
│   ├── doctors.json
│   ├── appointments.json
│   ├── inventory.json
│   └── billing.json
├── requirements.txt
└── README.md
```

- **app.py**: Main application file
- **data/**: Stores all data in JSON format

---

## 🛡️ Security & Privacy

- User authentication is required to access the system.
- All sensitive data is stored locally in JSON files.
- For production use, connect to a secure database.

---

## 📈 Analytics & Reporting

- Visualize patient statuses, revenue, and more
- Downloadable reports can be implemented in future updates

---

## 👩‍💻 Author

**Akhila Pathri**  
[GitHub](https://github.com/AkhilaPathri)

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/python/)

---

## 📜 License

This project is open-source for learning and demonstration.  
For commercial or production use, please contact the author.
