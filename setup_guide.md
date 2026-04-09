# 📦 Project Setup Guide

This document provides step-by-step instructions to clone, set up, and run the project in a local development environment.

---

## 🚀 Prerequisites

Ensure the following are installed:

* Python (>= 3.8 recommended)
* MongoDB
* Git
* `pip` (Python package manager)

---

## 📥 1. Clone Repository  

### Using HTTPS

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### Using SSH

```bash
git clone git@github.com:your-username/your-repo.git
cd your-repo
```

---

## ⚙️ 2. Start MongoDB Service

### Linux

```bash
sudo systemctl start mongod
```

### macOS (Homebrew)

```bash
brew services start mongodb-community
```

### Windows

```powershell
net start MongoDB
```

---

## 🐍 3. Create Virtual Environment  

### Linux / macOS

```bash
python3 -m venv venv
```

### Windows

```powershell
python -m venv venv
```

---

## ▶️ 4. Activate Virtual Environment  

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```powershell
venv\Scripts\activate
```

---

## 📦 5. Install Dependencies  

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🗄️ 6. Apply Migrations

```bash
python manage.py migrate
```

---

## 👤 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

## ▶️ 8. Run Django Development Server

```bash
python manage.py runserver
```

---

## 🌐 Access the Application

Open your browser and go to:

```
http://127.0.0.1:8000/
```

---

## ✅ Setup Checklist

* [ ] Repository cloned
* [ ] MongoDB service running
* [ ] Virtual environment created
* [ ] Virtual environment activated
* [ ] Dependencies installed
* [ ] Database migrations applied
* [ ] Development server running

---

## ⚠️ Additional Notes

* Configure MongoDB connection settings in your project.
* Add a `.env` file if your project depends on environment variables.
* Use `deactivate` to exit the virtual environment.

---

## 🛠 Troubleshooting

* **Git issues (SSH)**: Ensure SSH keys are configured (`ssh-keygen` + add to GitHub).
* **MongoDB not starting**: Verify installation and service status.
* **Module errors**: Ensure virtual environment is active.
* **Port already in use**:

  ```bash
  python manage.py runserver 8001
  ```

---

