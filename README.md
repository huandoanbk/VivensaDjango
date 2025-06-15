
# 🔮 Vivensa Backend

**Vivensa Backend** is a Django-based API server that powers the frontend of Vivensa – a numerology web application.  
It processes user data, calculates numerology results, generates AI-based introductions using Azure OpenAI, and returns structured results via API.

---

## ✨ Features

- Accepts **first name**, **last name**, and **birth date** from the frontend
- Calculates multiple **numerology core numbers**
- Stores results with a **public ID** and calculated values
- Communicates with **Azure OpenAI** to generate personalized report introductions
- Returns numerology insights via **REST API**
- Sends email via **SMTP** for the Contact form

---

## 📁 Project Structure

```
NUMAPPBACK/
├── contact/                 # Contact form and email logic
├── myenv/                   # (your local virtual environment, usually excluded from git)
├── numAppBack/              # Main Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── numerology/          # Numerology logic and models
├── .env                     # Environment variables (not committed)
├── .env.example             # Example env file
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## ⚙️ System Requirements

- Python **3.10+**
- Django **4.x**
- PostgreSQL
- Azure OpenAI

---

## 🚀 Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/huandoanbk/VivensaDjango.git
cd VivensaDjango
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv myenv
source myenv/bin/activate        # On Windows: myenv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL and Import SQL Database

> **Note**: This project uses a pre-configured database schema and content.  
You must manually **import the SQL data** instead of running Django migrations.

- Create a PostgreSQL database (e.g., `vivensa_db`)
- Import the `.sql` dump file into it

```bash
psql -U your_db_user -d vivensa_db < path_to_dump.sql
```

### 5. Create and Configure `.env` File

Use the provided `.env.example` as a base:

```bash
cp .env.example .env
```

Then, fill in the necessary values:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=vivensa_db
DB_USER=your_user
DB_PASSWORD=your_password
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
OPENAI_KEY=your_openai_key
```

### 6. Create Django Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Access your API at: `http://127.0.0.1:8000/`

---

## 🧑 Author

Developed by **Lari Doan**  
For questions or suggestions, contact: `contact@vivensa.fi`

---
