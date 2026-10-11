from flask import Blueprint, render_template

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.get("/callback")
def callback():
    return render_template("auth/callback.html")

@auth_bp.get("/register")
def signup():
    return render_template("auth/register.html")


@auth_bp.get("/login")
def login():
    return render_template("auth/loginn.html")

@auth_bp.get("/set-password")
def set_password():
    return render_template("auth/set_password.html")

@auth_bp.get("/reset-password")
def reset_password():
    return render_template("auth/reset_password.html")


@auth_bp.get("/employerregister")
@auth_bp.get("/emregister")
def emregister():
    return render_template("auth/emregister.html")

@auth_bp.get("/employerlogin")
@auth_bp.get("/emlogin")
def emlogin():
    return render_template("auth/emlogin.html")

@auth_bp.get("/seekerdashboard")
def seekerdashboard():
    from app.routes.main import get_jobs
    seeker = {"name": "Job Seeker", "profile_completion": 40}
    stages = ["Applied", "Screening", "Interview", "Offer"]
    posted_jobs = get_jobs()
    return render_template(
        "auth/seeker_dashboard.html",
        seeker=seeker,
        applications=[],
        saved=[],
        stages=stages,
        pipeline_counts={},
        posted_jobs=posted_jobs,
    )


@auth_bp.get("/employerdashboard")
def employerdashboard():
    from app.routes.main import get_jobs
    all_jobs = get_jobs()
    # Format each job to have views and applications_count for display
    formatted_jobs = []
    for idx, j in enumerate(all_jobs):
        job_copy = dict(j)
        job_copy["status"] = job_copy.get("status", "Approved")
        job_copy["views"] = job_copy.get("views", 18 + (idx * 14))
        job_copy["applications_count"] = job_copy.get("applications_count", 2 + (idx * 3))
        job_copy["posted_date"] = job_copy.get("posted_date", "Recently")
        formatted_jobs.append(job_copy)

    employer = {"company": "Your Company", "initials": "YC", "color": "#6C5CF5"}
    return render_template(
        "auth/employer_dashboard.html",
        employer=employer,
        my_jobs=formatted_jobs,
        total_apps=sum(j["applications_count"] for j in formatted_jobs) if formatted_jobs else 0,
        total_views=sum(j["views"] for j in formatted_jobs) if formatted_jobs else 0,
        shortlisted=len(formatted_jobs),
    )


@auth_bp.get("/plans")
@auth_bp.get("/employerplans")
def employerplans():
    return render_template("auth/employer_plans.html")


@auth_bp.get("/seekerplans")
def seekerplans():
    return render_template("auth/seeker_plans.html")


import os
import json
import random
import string
from flask import request, jsonify
from app.email_utils import send_employer_id_email

EMPLOYER_IDS_FILE = "employer_ids.json"

def get_employer_ids():
    if os.path.exists(EMPLOYER_IDS_FILE):
        with open(EMPLOYER_IDS_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_employer_ids(data):
    with open(EMPLOYER_IDS_FILE, "w") as f:
        json.dump(data, f)

def generate_employer_id():
    return "EMP-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

@auth_bp.post("/api/send_employer_id")
def send_employer_id():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400
        
    employer_ids = get_employer_ids()
    
    # Check if this email already has an ID assigned
    emp_id = None
    for existing_email, data_dict in employer_ids.items():
        if existing_email == email:
            emp_id = data_dict["employer_id"]
            break
            
    if not emp_id:
        # Generate a truly unique ID
        while True:
            emp_id = generate_employer_id()
            if not any(d["employer_id"] == emp_id for d in employer_ids.values()):
                break
        employer_ids[email] = {"employer_id": emp_id, "verified": False}
        save_employer_ids(employer_ids)
        
    success = send_employer_id_email(email, emp_id)
    if success:
        return jsonify({"message": "Employer ID sent to email successfully"})
    else:
        return jsonify({"error": "Failed to send email. Please check server logs."}), 500

@auth_bp.post("/api/verify_employer_id")
def verify_employer_id():
    data = request.get_json()
    email = data.get("email")
    emp_id = data.get("employer_id")
    
    if not email or not emp_id:
        return jsonify({"error": "Email and Employer ID are required"}), 400
        
    employer_ids = get_employer_ids()
    
    if email not in employer_ids:
        return jsonify({"error": "No Employer ID requested for this email"}), 400
        
    if employer_ids[email]["employer_id"] == emp_id:
        employer_ids[email]["verified"] = True
        save_employer_ids(employer_ids)
        return jsonify({"message": "Employer ID verified successfully"})
    else:
        return jsonify({"error": "Invalid Employer ID"}), 400

REGISTERED_EMPLOYERS_FILE = "registered_employers.json"

@auth_bp.post("/api/save_employer_profile")
def save_employer_profile():
    data = request.get_json()
    employer_id = data.get("employer_id")
    
    if not employer_id:
        return jsonify({"error": "Employer ID required"}), 400
        
    # Load existing
    employers = {}
    if os.path.exists(REGISTERED_EMPLOYERS_FILE):
        with open(REGISTERED_EMPLOYERS_FILE, "r") as f:
            try:
                employers = json.load(f)
            except:
                pass
                
    # Save mapping: Employer ID -> full profile data
    employers[employer_id] = data
    
    with open(REGISTERED_EMPLOYERS_FILE, "w") as f:
        json.dump(employers, f, indent=4)
        
    return jsonify({"message": "Profile saved locally."})


import urllib.request
import ssl
from app.email_utils import send_password_reset_email

@auth_bp.post("/api/forgot_password")
def api_forgot_password():
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    if not email:
        return jsonify({"error": "Email is required"}), 400

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_secret = os.getenv("SUPABASE_SECRET_KEY")

    if not supabase_url or not supabase_secret:
        return jsonify({"error": "Supabase configuration is missing"}), 500

    # Call Supabase Admin API to generate recovery link
    admin_url = f"{supabase_url}/auth/v1/admin/generate_link"
    payload = json.dumps({
        "type": "recovery",
        "email": email,
        "redirect_to": "http://127.0.0.1:5000/auth/callback"
    }).encode("utf-8")

    req = urllib.request.Request(admin_url, data=payload, headers={
        "apikey": supabase_secret,
        "Authorization": f"Bearer {supabase_secret}",
        "Content-Type": "application/json"
    })

    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            link_data = json.loads(resp.read().decode())
            action_link = link_data.get("action_link")

            if not action_link:
                return jsonify({"error": "Could not generate recovery link."}), 500

            # Send via our branded Gmail SMTP
            sent = send_password_reset_email(email, action_link)
            if sent:
                return jsonify({"message": "Password reset email sent from NEXORA! Please check your inbox."})
            else:
                return jsonify({"error": "Failed to send email. Please check server SMTP configuration."}), 500
    except urllib.error.HTTPError as err:
        err_body = err.read().decode()
        try:
            err_json = json.loads(err_body)
            msg = err_json.get("msg") or err_json.get("message") or "User not found"
        except:
            msg = "User not found with this email address."
        return jsonify({"error": msg}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500