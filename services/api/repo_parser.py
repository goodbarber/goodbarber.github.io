import os
from services.utils.markdown_handler import *


def custom_sort(item):
    # Define key priority
    priority_keys = [
        "goodbarber-custom-features",
        "goodbarber-api-integrations",
        "goodbarber-internal-librairies",
    ]

    if item in priority_keys:
        # Higher priority
        return priority_keys.index(item)
    else:
        # Lower priority
        return len(priority_keys)


def create_context_for_template_engine(categories, categories_mapping):
    print("Processing template generation...")
    # Initialize context dictionary with categories list
    context = {"categories": []}

    # Iterate over each category name, sorted by custom sorting logic
    for category_name in sorted(categories.keys(), key=lambda item: custom_sort(item)):
        # Check if the category name exists in the mapping dictionary
        if category_name in categories_mapping.keys():
            # Prepare data dictionary for the category
            data = {
                "name": categories_mapping[category_name],
                "index": categories_mapping[category_name].lower(),
                "has_repos_with_images": False,
                "has_repos_without_images": False,
                "repos_with_images": [],
                "repos_without_images": [],
            }

            # Iterate over each repository in the current category, sorted alphabetically
            for repo_name, repo_data in sorted(categories[category_name].items()):
                title = extract_title_after_dash_first_line(repo_data["readme"])
                # Extract image from the README
                # image = extract_first_image(repo_data["readme"])

                # Create a dictionary for the repository's data
                repo = {
                    "title": title,
                    "real_name": repo_name,
                    "href": repo_data["html_url"],
                    "website": repo_data.get("homepage", None),
                    "description": repo_data.get("description", None),
                }

                # Check if an image exists for the repository and categorize accordingly
                if os.path.exists(os.path.join("repo_images", "%s.webp" % repo_name)):
                    data["repos_with_images"].append(repo)
                    data["has_repos_with_images"] = True
                else:
                    data["repos_without_images"].append(repo)
                    data["has_repos_without_images"] = True

            # Add the category data to the context
            context["categories"].append(data)
    
    print("Done! Enjoy ~.~")

    return context
