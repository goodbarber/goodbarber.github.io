import os
from services.utils.sorting import custom_sort
from services.utils.markdown_handler import *


def process_repositories(categories, prioritized_list, categories_mapping):
    context = {"categories": []}
    for category_name in sorted(categories.keys(), key=lambda item: custom_sort(item, prioritized_list)):
        data = {
            "name": categories_mapping[category_name],
            "index": categories_mapping[category_name].lower(),
            "has_repos_with_images": False,
            "has_repos_without_images": False,
            "repos_with_images": [],
            "repos_without_images": [],
        }
        for repo_name, repo_data in sorted(categories[category_name].items()):
            name = extract_text_after_dash_first_line(repo_data["readme"])
            repo = {
                "name": name,
                "href": repo_data["html_url"],
                "website": repo_data.get("homepage", None),
                "description": repo_data.get("description", None),
            }
            if os.path.exists(os.path.join("repo_images", "%s.jpg" % repo_name)):
                data["repos_with_images"].append(repo)
                data["has_repos_with_images"] = True
            else:
                data["repos_without_images"].append(repo)
                data["has_repos_without_images"] = True
        context["categories"].append(data)
    return context