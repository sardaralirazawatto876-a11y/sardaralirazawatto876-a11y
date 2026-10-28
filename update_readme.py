import re
import requests

USERNAME = "sardaralirazawatto876-a11y"

url = f"https://api.github.com/users/{USERNAME}/repos?sort=updated&per_page=10"

response = requests.get(
    url,
    headers={"Accept": "application/vnd.github+json"},
    timeout=30
)
response.raise_for_status()

repos = response.json()

project_list_md = ""
for repo in repos:
    name = repo["name"]
    if name.lower() == USERNAME.lower():
        continue

    repo_url = repo["html_url"]
    description = repo["description"] or "A software engineering project."
    language = repo["language"] or "Code"

    project_list_md += f"- **[{name}]({repo_url})** ({language}) — {description}\n"

if not project_list_md:
    project_list_md = "- *No public repositories found yet. Keep building!*\n"

with open("README.md", "r", encoding="utf-8") as f:
    readme_content = f.read()

pattern = r"(<!-- START_SECTION:projects -->\n)(.*?)(\n<!-- END_SECTION:projects -->)"
updated_content = re.sub(
    pattern,
    f"\\1{project_list_md}\\3",
    readme_content,
    flags=re.DOTALL
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated_content)

print("Profile README successfully updated!")
