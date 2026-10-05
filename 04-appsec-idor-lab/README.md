# IDOR (Insecure Direct Object Reference) Demonstration Lab

A lightweight, practical web application built with Python (Flask) and SQLite to demonstrate **Horizontal Privilege Escalation via IDOR**, alongside its secure, session-validated remediation.

## 🛠️ Tech Stack

- **Language:** Python 3
- **Framework:** Flask
- **Database:** SQLite

---

## 🔍 Understanding the Vulnerability

### The Flaw (`app_vulnerable.py`)

In insecure applications, server-side code often blindly trusts user input supplied via URL parameters (e.g., `?id=1`) without validating whether the currently authenticated user actually owns or has permission to view that resource.

**The Attack Vector:** An attacker logs in with their own valid account, but modifies the `id` parameter in the URL address bar to target another user's ID, allowing them to harvest private profile data, emails, and sensitive records.

### The Fix (`app_secure.py`)

To remediate an IDOR vulnerability, **never rely on client-supplied identifiers for authorization checks.**

**The Solution:** The application extracts the user's identity securely from an encrypted or server-side session state (`session['user_id']`) rather than trusting raw URL parameters.

---

## 📁 Project Structure

```
appsec-portfolio/04-appsec-idor-lab/
├── app_vulnerable.py      # Intentionally flawed endpoint vulnerable to horizontal privilege escalation
├── app_secure.py          # Patched implementation leveraging server-side session cookies
├── requirements.txt       # Project dependencies (Flask)
└── README.md              # This file
```

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/appsec-portfolio.git
cd appsec-portfolio/04-appsec-idor-lab
```

### 2. Set Up Virtual Environment and Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Test the Vulnerable App

```bash
python app_vulnerable.py
```

1. Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
2. Log in as `alice`
3. Change the URL parameter from `?id=1` to `?id=2`
4. **Observe:** Unauthorized data access (horizontal privilege escalation)

### 4. Test the Secure App

```bash
python app_secure.py
```

1. Open [http://127.0.0.1:5001/](http://127.0.0.1:5001/)
2. Log in with any user account
3. Attempt to change the URL parameter to access another user's data
4. **Observe:** The app safely restricts data access using backend session validation regardless of URL input

---

## 🎯 Learning Objectives

By completing this lab, you will:

- Understand how IDOR vulnerabilities enable horizontal privilege escalation
- Recognize insecure patterns that trust client-supplied identifiers
- Learn to implement proper session-based authorization checks
- Practice identifying and remediating IDOR flaws in web applications

---

## ⚠️ Security Warning

**This application is intentionally vulnerable for educational purposes only.** Do not deploy `app_vulnerable.py` to production or any publicly accessible environment. Use only in isolated, local testing environments.

---

## 📚 Additional Resources

- [OWASP Top 10 - Broken Access Control](https://owasp.org/www-project-top-ten/)
- [PortSwigger - IDOR Vulnerabilities](https://portswigger.net/web-security/access-control/idor)
- [CWE-639: Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html)

---

## 🤝 Contributing

Feel free to fork this repository and submit pull requests with improvements or additional security demonstrations.

---

## 📄 License

This project is open source and available for educational use.
