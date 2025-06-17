from typing import Dict, List


def match_job(job: Dict, skills: List[str]) -> Dict:
    """Return match score and matched skills."""
    description = (job.get("body") or "").lower()
    matched = [s for s in skills if s.lower() in description]
    score = len(matched)
    return {"score": score, "matched_skills": matched}
