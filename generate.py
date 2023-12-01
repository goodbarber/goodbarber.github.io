#!/usr/bin/env python

from services.api_github import GitHubClient
from services.utils.file_handler import *
from services.repo_parser import *


def main():
    client = GitHubClient()
    template = load_template("index.mustache")
    categories = client.gh_repos()
    prioritized_list = ["goodbarber-appsdk", "goodbarber-plugin", "android"]
    categories_mapping = {
        "goodbarber-appsdk": "Custom Features",
        "goodbarber-plugin": "API integrations",
        "android": "Internal Libraries",
    }

    context = process_repositories(categories, prioritized_list, categories_mapping)
    renderer = pystache.Renderer()
    html = renderer.render(template, context)
    save_html("index.html", html)


if __name__ == "__main__":
    main()
