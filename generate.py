#!/usr/bin/env python

from services.api.github import GitHubClient
from services.utils.file_handler import *
from services.api.repo_parser import *


def main():
    client = GitHubClient()
    template = load_template("index.mustache")
    repos_by_categories = client.gh_repos()
    categories_mapping = {
        "goodbarber-custom-features": "Custom features",
        "goodbarber-api-integrations": "API integrations",
        "goodbarber-internal-librairies": "Internal libraries",
    }

    context = process_repositories(repos_by_categories, categories_mapping)
    renderer = pystache.Renderer()
    html = renderer.render(template, context)
    save_html("index.html", html)


if __name__ == "__main__":
    main()
