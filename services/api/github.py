import netrc
import time
from github import Github


class GitHubClient:
    def __init__(self):
        # Initialize GitHub client and login status
        self.ghclient = None
        self.logged_in = False
        self.login()

    def login(self):
        try:
            # Attempt to login using credentials from .netrc
            auth = netrc.netrc()
            (user, _, token) = auth.authenticators("api.github.com")
            self.ghclient = Github(token)
            self.logged_in = True
            print("Logged in")
        except Exception as e:
            # If login fails, set client without authentication
            self.ghclient = Github()
            self.logged_in = False
            print(f"Not logged in with error : {e}")

    def gh_repos(self):
        if not self.logged_in:
            # Check if the user is logged in
            print("Not logged in. Please login to GitHub.")
            # Pause to avoid GitHub rate limiting
            time.sleep(2.0)
            return None

        # Fetches all repositories information
        try:
            print("Fetching all repos informations and performing magic on them...")
            repos_formatted_by_categories = {}
            repos = self.ghclient.get_user().get_repos()
            # Filter repos without topics
            filtered_repos = [repo for repo in repos if repo.topics]
            # Load READMEs
            readmes = {
                repo.name: self.ghclient.get_user().get_repo(repo.name).get_readme()
                for repo in filtered_repos
            }

            for repo in filtered_repos:
                # Organize repositories by topics
                for topic in repo.topics:
                    repo_info = dict(
                        homepage=repo.homepage,
                        html_url=repo.html_url,
                        description=repo.description,
                        readme=readmes[repo.name],
                    )
                    if topic not in repos_formatted_by_categories:
                        repos_formatted_by_categories[topic] = {}
                    repos_formatted_by_categories[topic][repo.name] = repo_info
            return repos_formatted_by_categories

        except Exception as e:
            print(f"Error : {e}")
            return None
