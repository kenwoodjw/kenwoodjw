import os
from github import Github
import re

def update_readme_with_pr_stats():
    g = Github(os.getenv('GITHUB_TOKEN'))
    user = g.get_user()
    
    pr_stats = {}
    for pr in prs:
        repo_name = pr.repository.full_name
        stars = pr.repository.stargazers_count
        pr_date = pr.created_at
        
        if repo_name not in pr_stats or pr_date > pr_stats[repo_name]['last_pr_date']:
            pr_stats[repo_name] = {
                'count': pr_stats.get(repo_name, {}).get('count', 0) + 1,
                'stars': stars,
                'last_pr_date': pr_date
            }
        else:
            pr_stats[repo_name]['count'] += 1
    
    sorted_stats = dict(sorted(pr_stats.items(), key=lambda x: x[1]['stars'], reverse=True))
    
    pr_table = "## 🌟 Top 10 Most Popular Repos I've Contributed To\n\n"
    pr_table += "| Repository | Stars | PR Count | Last PR |\n"
    pr_table += "|------------|---------------|-------|---------||\n"
    
    for repo, stats in list(sorted_stats.items())[1:11]:
        pr_table += f"| [{repo}](https://github.com/{repo}) | {stats['stars']} | {stats['count']} | {stats['last_pr_date'].strftime('%Y-%m-%d')} |\n"
    

    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    pr_section_pattern = r'## 🌟 Top 10 Most Popular Repos[\s\S]*?(?=##|$)'
    if re.search(pr_section_pattern, content):
        content = re.sub(pr_section_pattern, pr_table, content)
    else:
        content += '\n\n' + pr_table

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    update_readme_with_pr_stats()