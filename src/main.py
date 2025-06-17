from pathlib import Path
import json
from datetime import datetime
from typing import List

from config import PROFILE, GITHUB_REPO
from scraper import get_open_issues, parse_issue
from matcher import match_job
from resume_generator import generate_resume

DATA_DIR = Path("data")
JOB_DIR = DATA_DIR / "jobs"
RESUME_DIR = DATA_DIR / "resumes"
JOB_DIR.mkdir(parents=True, exist_ok=True)
RESUME_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_FILE = DATA_DIR / "processed_jobs.json"


try:
    processed = json.loads(PROCESSED_FILE.read_text())
except Exception:
    processed = []

issues = get_open_issues(GITHUB_REPO)
new_processed = processed.copy()

for issue in issues:
    job = parse_issue(issue)
    job_id = job["id"]
    if job_id in processed:
        continue
    match = match_job(job, PROFILE["skills"])
    job_path = JOB_DIR / f"{job_id}.md"
    job_path.write_text(job["body"] or "")
    if match["score"] > 0:
        resume_path = RESUME_DIR / f"resume_{job_id}.tex"
        generate_resume(PROFILE, match, job, resume_path)
    new_processed.append(job_id)

PROCESSED_FILE.write_text(json.dumps(new_processed, indent=2))
