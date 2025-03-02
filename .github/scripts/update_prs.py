import os
from github import Github
import re

def update_readme_with_pr_stats():
    g = Github(os.getenv('GITHUB_TOKEN'))
    user = g.get_user()
    
    pr_stats = {}
    # search for PRs authored by the current user(excluding self)
    query = f"is:pr author:{user.login} -user:{user.login}"
    
    prs = g.search_issues(query)
    
    for pr in prs:
        repo_name = pr.repository.full_name
        pr_stats[repo_name] = pr_stats.get(repo_name, 0) + 1
    
    sorted_stats = dict(sorted(pr_stats.items(), key=lambda x: x[1], reverse=True))
    
    pr_table = "## My Pull Requests\n\n"
    pr_table += "| Repository | Pull Requests |\n"
    pr_table += "|------------|---------------|\n"
    
    for repo, count in sorted_stats.items():
        pr_table += f"| [{repo}](https://github.com/{repo}) | {count} |\n"
    

    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    pr_section_pattern = r'## My Pull Requests[\s\S]*?(?=##|$)'
    if re.search(pr_section_pattern, content):
        content = re.sub(pr_section_pattern, pr_table, content)
    else:
        content += '\n\n' + pr_table
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    update_readme_with_pr_stats()