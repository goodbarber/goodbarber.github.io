#!/usr/bin/env python

from collections import defaultdict
import netrc
import time
import json
import codecs
import pystache
import os

from pygithub3 import Github

repos_in = "repos.json"
template_in = "index.mustache"
index_out = "index.html"

categories_mapping = {
    "goodbarber-appsdk": "Custom Features",
    "goodbarber-plugin": "API integrations",
    "android": "Internal Libraries",
}

auth = netrc.netrc()
print(auth)

try:
    (user, _, token) = auth.authenticators("api.github.com")
    ghclient = Github(token)
    logged_in = True
    print("Logged in")
except Exception as e:
    ghclient = Github()
    logged_in = False
    print(f"Not logged in with error : {e}")


def gh_repo(name):
    print("Fetching repo information...")

    if not logged_in:
        print("Not logged in.  Please login to GitHub.")
        # Take a nap so GitHub doesn't aggressively throttle us.
        time.sleep(2.0)

    repo = ghclient.get_user().get_repo(name)
    return dict(
        name=repo.name,
        homepage=repo.homepage,
        html_url=repo.html_url,
        description=repo.description,
    )


with codecs.open(template_in, "r", "utf-8") as f:
    template = pystache.parse(f.read())
with codecs.open(repos_in, "r", "utf-8") as f:
    repos = json.loads(f.read())

# Multimap of categories to their repos.
categories = defaultdict(list)

for repo in repos:
    repo_cats = repos[repo]
    repo_data = gh_repo(repo)
    if repo_cats is None or len(repo_cats) == 0:
        continue
    for cat in repo_cats:
        categories[cat].append(repo_data)

# Template context that will be used for rendering.
context = {"categories": []}

# Loop over the category names sorted alphabetically (case-insensitive) with 'Other' last.
# for category_name in sorted(
#     categories.keys(), key=lambda s: s.lower() if s != "Other" else "z" * 10
# ):

# Prioritize specific names by assigning them a lower index.
prioritized = ["goodbarber-appsdk", "goodbarber-plugin", "android"]


def custom_sort(key):
    try:
        # Prioritize specific names by assigning them a lower index
        return prioritized.index(key)
    except ValueError:
        # For other names, use a high index followed by the normal key
        return len(prioritized), key.lower()


print(categories.keys())
print(sorted(categories.keys(), key=custom_sort))

for category_name in sorted(categories.keys(), key=custom_sort):
    data = {
        "name": categories_mapping[category_name],
        "index": categories_mapping[category_name].lower(),
        "has_repos_with_images": False,
        "has_repos_without_images": False,
        "repos_with_images": [],
        "repos_without_images": [],
    }

    # Loop over category repos sorted alphabetically (case-insensitive).
    for repo_data in sorted(
        categories[category_name], key=lambda s: s["name"].capitalize()
    ):
        # Mock examples
        for _ in range(8):
            if category_name == "goodbarber-appsdk":
                name = "Booking Widget"
                repo = {
                    "name": name,
                    "href": "XXXXXXXXXXX",
                    "website": "XXXXXXXXXXXXXXX",
                    "description": "In-App Purchase represents nearly 50% of the revenue generated by native apps. Discover in-app purchases and their key features.",
                }
            elif category_name == "goodbarber-plugin":
                name = "Integration_name"
                repo = {
                    "name": name,
                    "href": "XXXXXXXXXXX",
                    "website": "XXXXXXXXXXXXXXX",
                    "description": "Approximate Nearest Neighbors in C++/ Python optimized for memory usage and loading/saving to disk.",
                }
            elif category_name == "android":
                name = "Library_name"
                repo = {
                    "name": name,
                    "href": "XXXXXXXXXXX",
                    "website": "XXXXXXXXXXXXXXX",
                    "description": "Approximate Nearest Neighbors in C++/ Python optimized for memory usage and loading/saving to disk.",
                }   
            # End mock examples

            # name = repo_data["name"]
            # repo = {
            #     "name": name,
            #     "href": repo_data["html_url"],
            #     "website": repo_data.get("homepage", None),
            #     "description": repo_data.get("description", None),
            # }
            if os.path.exists(os.path.join("repo_images", "%s.jpg" % name)):
                data["repos_with_images"].append(repo)
                data["has_repos_with_images"] = True
            else:
                data["repos_without_images"].append(repo)
                data["has_repos_without_images"] = True

    context["categories"].append(data)

# Render the page HTML using MOOOUUSSTTAACCCCHHEEEEE!
renderer = pystache.Renderer()
html = renderer.render(template, context)

with codecs.open(index_out, "w", "utf-8") as f:
    f.write(html)
