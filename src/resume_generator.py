from pathlib import Path
from typing import Dict, List
from jinja2 import Template

TEMPLATE = r"""
\documentclass{article}
\usepackage[margin=1in]{geometry}
\begin{document}
\begin{center}
    {\LARGE \textbf{ {{ name }} }}\\
    {{ email }} \\ {{ phone }}
\end{center}

\section*{Skills}
\begin{itemize}
{% for skill in skills %}
    \item {{ skill }}
{% endfor %}
\end{itemize}

\section*{Experience}
{% for exp in experience %}
\textbf{ {{ exp.role }} } -- {{ exp.company }} ({{ exp.duration }})\\
{{ exp.description }}\\
\medskip
{% endfor %}

\section*{Job Alignment}
Job Title: {{ job_title }}\\
Company: {{ company }}\\
Score: {{ score }}\\
Matched Skills: {{ matched_skills|join(', ') }}
\end{document}
"""


def generate_resume(profile: Dict, match: Dict, job: Dict, output_path: Path) -> None:
    template = Template(TEMPLATE)
    tex = template.render(
        name=profile["name"],
        email=profile["email"],
        phone=profile["phone"],
        skills=profile["skills"],
        experience=profile["experience"],
        job_title=job["title"],
        company=job.get("company", "Unknown"),
        score=match["score"],
        matched_skills=match["matched_skills"],
    )
    output_path.write_text(tex)
