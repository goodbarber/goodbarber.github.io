#!/usr/bin/env python

from services.api.github import GitHubClient
from services.utils.file_handler import *
from services.api.repo_parser import *


def main():
    client = GitHubClient()

    # Load template for parsing
    template = load_template("index.mustache")

    # Get all repos informations
    repos_by_categories = client.gh_repos()

    # This is where we define the categories that will be processed
    categories_mapping = {
        "goodbarber-custom-features": "Custom features",
        "goodbarber-api-integrations": "API integrations",
        "goodbarber-internal-librairies": "Internal libraries",
    }

    # Create context for pystach engine
    context = create_context_for_template_engine(
        repos_by_categories, categories_mapping
    )
    renderer = pystache.Renderer()
    html = renderer.render(template, context)
    save_html("index.html", html)


if __name__ == "__main__":
    main()
