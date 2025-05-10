
# 🏥 Hospital Management System (HMS)

A web-based Hospital Management System built using Django. This project is designed to simplify hospital operations such as patient registration, doctor management, appointments, and more.

## 🚀 Features

- Patient registration and record management  
- Doctor module with scheduling  
- Appointment booking and tracking  
- Admin panel for system control  
- Responsive user interface

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Database:** MySQL (via XAMPP)
- **Frontend:** HTML, CSS, Bootstrap (or as used)
- **Tools:** VS Code, Git, XAMPP

## 🧑‍💻 How to Run

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/hms.git
   cd hms
   ```

2. **Set up a virtual environment**

   ```bash
   python -m venv env
   env\Scripts\activate  # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL using XAMPP**
   - Create a database (e.g., `hms_db`)
   - Update `settings.py` with your DB credentials

5. **Run migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the server**

   ```bash
   python manage.py runserver
   ```

7. Visit: [http://localhost:8000](http://localhost:8000)

## 📁 Project Structure

```
hms/
├── hms/                 # Project settings
├── hospital/            # Main app
├── templates/           # HTML templates
├── static/              # CSS, JS, Images
├── db.sqlite3           # SQLite DB (optional)
├── manage.py
└── README.md
```

## 📄 License

This project is licensed under the MIT License.

---

**Developed by:** 
Tarun Attri
Saiyam Jain
Harshit Pathak
Sachin Yadav

