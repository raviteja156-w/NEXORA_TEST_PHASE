from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/jobs")
def jobs():
    all_jobs = get_jobs()
    
    formatted_jobs = []
    for j in all_jobs:
        item = dict(j)
        item["is_employer_posted"] = True
        item["company_color"] = "linear-gradient(135deg, #6C5CF5, #2BE0BE)"
        item["company_initials"] = (item.get("title") or "J")[:2].upper()
        item["match_score"] = 96
        formatted_jobs.append(item)
        
    curated_jobs = [
        {
            "id": "featured-1",
            "title": "Software Engineer",
            "company": "Microsoft",
            "company_initials": "MS",
            "company_color": "#00A4EF",
            "location": "Sydney / Hybrid",
            "type": "Full Time",
            "salary_min": "130000",
            "salary_max": "155000",
            "description": "Join our cloud engineering team building scalable enterprise microservices using Python, Flask, and Azure.",
            "requirements": "Python, Flask, SQL, Cloud Architecture",
            "match_score": 94
        },
        {
            "id": "featured-2",
            "title": "Python Backend Developer",
            "company": "Amazon",
            "company_initials": "AM",
            "company_color": "#FF9900",
            "location": "Melbourne / Remote",
            "type": "Full Time",
            "salary_min": "140000",
            "salary_max": "165000",
            "description": "Develop high-throughput data processing pipelines and RESTful microservices for AWS customer platforms.",
            "requirements": "Python, Django, AWS, PostgreSQL",
            "match_score": 90
        },
        {
            "id": "featured-3",
            "title": "Associate Software Engineer",
            "company": "TCS",
            "company_initials": "TC",
            "company_color": "#E94E34",
            "location": "Brisbane / Full Time",
            "type": "Full Time",
            "salary_min": "95000",
            "salary_max": "115000",
            "description": "Work with cross-functional teams delivering modern web solutions and automated test suites.",
            "requirements": "Python, SQL, OOP, REST APIs",
            "match_score": 85
        },
        {
            "id": "featured-4",
            "title": "Frontend Engineer",
            "company": "Canva",
            "company_initials": "CV",
            "company_color": "#00C4CC",
            "location": "Sydney / Hybrid",
            "type": "Full Time",
            "salary_min": "125000",
            "salary_max": "145000",
            "description": "Craft intuitive, performant user interfaces used by millions of creators worldwide.",
            "requirements": "JavaScript, HTML5, CSS3, Modern UI",
            "match_score": 88
        }
    ]
    
    return render_template("jobs.html", jobs=formatted_jobs + curated_jobs)



import os
import json
import uuid
from flask import request, jsonify, render_template

JOBS_FILE = "jobs.json"

def get_jobs():
    if os.path.exists(JOBS_FILE):
        with open(JOBS_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_jobs(jobs):
    with open(JOBS_FILE, "w") as f:
        json.dump(jobs, f, indent=4)

@main.route("/post-job", methods=["GET", "POST"])
def post_job():
    if request.method == "POST":
        data = request.get_json(silent=True)
        if not data and request.form:
            data = request.form.to_dict()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        jobs = get_jobs()
        
        salary_str = data.get("salary")
        if not salary_str:
            s_min = data.get("salary_min")
            s_max = data.get("salary_max")
            if s_min and s_max:
                salary_str = f"${s_min} - ${s_max}"
            elif s_min:
                salary_str = f"From ${s_min}"
            else:
                salary_str = "Competitive"

        new_job = {
            "id": str(uuid.uuid4()),
            "title": data.get("title", "Untitled Position"),
            "company": data.get("company") or "Nexora Hiring Partner",
            "type": data.get("type", "Full-time"),
            "location": data.get("location", "Remote"),
            "salary_min": data.get("salary_min"),
            "salary_max": data.get("salary_max"),
            "salary": salary_str,
            "description": data.get("description", ""),
            "requirements": data.get("requirements", ""),
            "employer_id": data.get("employer_id"),
            "posted_date": "Just now",
            "status": "Active"
        }
        
        jobs.append(new_job)
        save_jobs(jobs)
        
        if request.is_json:
            return jsonify({"message": "Job posted successfully", "job_id": new_job["id"]})
        else:
            from flask import redirect, url_for
            return redirect(url_for("auth.employerdashboard"))
        
    return render_template("post_job.html")


@main.route("/applicants")
def applicants():
    # TODO: replace with a real applicants list for the logged-in employer.
    return render_template("index.html")


@main.route("/pricing")
def pricing():
    # TODO: replace with a real pricing page.
    return render_template("index.html")