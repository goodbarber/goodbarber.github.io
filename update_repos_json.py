#!/usr/bin/env python

import netrc
import time
import json

from services.api.github import GitHubClient

repos_out = "repos.json"

client = GitHubClient()

def gh_repos():
    print("Fetching all repos informations...")

    if not client.logged_in:
        print("Not logged in.  Please login to GitHub.")
        # Take a nap so GitHub doesn't aggressively throttle us.
        time.sleep(2.0)
    try:
        repos = client.ghclient.get_user().get_repos()
        repos_formatted = {repo.name: repo.topics for repo in repos}

        with open(repos_out, "w") as f:
            json.dump(repos_formatted, f, indent=4)
    except Exception as e:
        print(f"Error : {e}")


gh_repos()
