# 🔍 NetRecon — Network Reconnaissance Web Application

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?style=flat-square&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=flat-square&logo=sqlite)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Termux-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

> A full-stack web application for performing and logging network reconnaissance tasks — built as a hands-on cybersecurity portfolio project.

---

## 📌 About the Project

NetRecon is a **Flask-based web application** that allows users to perform basic network reconnaissance operations through a clean browser interface. It was built from scratch as part of a self-directed ethical hacking and cybersecurity learning journey — entirely on **Android using Termux**, without a laptop.

This project demonstrates practical skills in:
- Backend development with Python & Flask
- Database integration using SQLAlchemy + SQLite
- Building security-focused tools with a real-world use case
- Running a full dev environment on a mobile device (Termux + proot)

---

## ⚙️ Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Backend    | Python 3, Flask         |
| Database   | SQLite + SQLAlchemy ORM |
| Frontend   | HTML, CSS, JavaScript   |
| Platform   | Linux (Termux / proot)  |

---

## 🚀 Features

- 🔎 **Host/IP Reconnaissance** — Perform basic recon operations on target hosts
- 📋 **Scan Logging** — All results stored in SQLite via SQLAlchemy for review
- 🌐 **Web Interface** — Clean browser-based UI, no command line needed for users
- 📁 **Modular Flask Structure** — Organized routes, models, and templates
- 🐧 **Termux Compatible** — Built and tested entirely on Android (Arch Linux proot)

---

## 🗂️ Project Structure

```
netrecon/
├── backend/
│   └── app.py          # Main Flask application
├── templates/          # HTML templates
├── static/             # CSS & JS files
└── README.md
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.x
- pip
- Flask, SQLAlchemy

### Steps

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/netrecon.git
cd netrecon

# Install dependencies
pip install flask sqlalchemy

# Run the application
cd backend
python app.py
```

Then open your browser and navigate to `http://localhost:5000`

---

## ⚠️ Disclaimer

> This tool is intended for **educational purposes only**.
> Only use NetRecon on systems you own or have **explicit written permission** to test.
> Unauthorized scanning of networks is illegal and unethical.
> The developer is not responsible for any misuse of this tool.

---

## 🎯 Learning Goals Achieved

This project was built to demonstrate the following skills:

- [x] Python web development with Flask
- [x] ORM-based database design with SQLAlchemy
- [x] Full-stack integration (backend + frontend)
- [x] Cybersecurity tool design principles
- [x] Linux environment setup and management on mobile (Termux)
- [x] REST API structure and routing

---

## 👤 Author

**Cherry**
📍 Visakhapatnam, Andhra Pradesh, India
🎓 Final Year Diploma — Computer Engineering
🔐 Aspiring Ethical Hacker & Cybersecurity Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/YOUR_PROFILE)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat-square&logo=github)](https://github.com/YOUR_USERNAME)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
