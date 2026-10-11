# Nexora

> A modern job-seeking and recruitment platform connecting job seekers and employers.

## About Nexora

**Nexora** is a web-based job platform designed to simplify the process of finding jobs and recruiting talent.

The platform provides dedicated experiences for **Job Seekers** and **Employers**, allowing users to manage profiles, discover opportunities, post jobs, and manage applications through a centralized system.

---

## Key Features

### Job Seekers

* User registration and authentication
* Personal profile management
* Professional information and profile details
* Resume management
* Browse job opportunities
* Search and filter jobs
* View detailed job information
* Apply for jobs
* Track job applications

### Employers

* Employer registration and authentication
* Company profile management
* Create and manage job postings
* View job applicants
* Manage applications
* Employer dashboard

### Platform

* Role-based user system
* Database-backed user and job management
* Secure environment-variable configuration
* Responsive web interface
* Separate dashboards for different user roles

---

## Technology Stack

| Layer           | Technology            |
| --------------- | --------------------- |
| Backend         | Python, Flask         |
| Frontend        | HTML, CSS, JavaScript |
| Database        | SQL / PostgreSQL      |
| Version Control | Git, GitHub           |
| Development     | Visual Studio Code    |

---


## Environment Configuration

Nexora uses environment variables for configuration and credentials.

Create a `.env` file in the project root:

```env
DATABASE_URL=
SECRET_KEY=
API_KEY=
```

Never commit real credentials or API keys to the repository.

Use `.env.example` as a reference for required environment variables.

---

## Installation

### Clone the repository

```bash
git clone https://github.com/manohar-dev11/Nexora.git
cd Nexora
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create your `.env` file and add the required configuration values.

### Run the application

```bash
python app.py
```

Open the local Flask URL in your browser.

---

## Project Goal

Nexora aims to provide a simple and centralized platform where **job seekers can discover career opportunities** and **employers can find and manage potential candidates**.

---

## Repository

**GitHub:**
https://github.com/manohar-dev11/Nexora

---

## License


