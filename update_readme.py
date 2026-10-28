import os
import re
import requests

# 1. Fetch public repositories from GitHub API
USERNAME = "sardaralirazawatto876-a11y"
url = f"https://github.com{USERNAME}/repos?sort=updated&per_page=10"

response = requests.get(url)
repos = response.json()

# 2. Build the markdown list of projects
project_list_md = ""
for repo in repos:
    name = repo["name"]
    # Skip the profile README repository itself
    if name.lower() == USERNAME.lower():
        continue
    
    url = repo["html_url"]
    description = repo["description"] or "A software engineering project."
    language = repo["language"] or "Code"
    
    project_list_md += f"- **[{name}]({url})** ({language}) — {description}\n"

if not project_list_md:
    project_list_md = "- *No public repositories found yet. Keep building!*\n"

# 3. Read current README and replace content between placeholder comments
with open("README.md", "r", encoding="utf-8") as f:
    readme_content = f.read()

pattern = r"(<!-- START_SECTION:projects -->\n)(.*?)(\n<!-- END_SECTION:projects -->)"
updated_content = re.sub(
    pattern, 
    f"\\1{project_list_md}\\3", 
    readme_content, 
    flags=re.DOTALL
)

# 4. Save the updated README file
with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated_content)

print("Profile README successfully updated!")
