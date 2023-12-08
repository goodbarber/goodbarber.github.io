import netrc
import time
from github import Github

class GitHubClient:
    def __init__(self):
        self.ghclient = None
        self.logged_in = False
        self.login()

    def login(self):
        try:
            auth = netrc.netrc()
            (user, _, token) = auth.authenticators("api.github.com")
            self.ghclient = Github(token)
            self.logged_in = True
            print("Logged in")
        except Exception as e:
            self.ghclient = Github()
            self.logged_in = False
            print(f"Not logged in with error : {e}")

    def gh_repos(self):
        print("Fetching all repos informations...")
        if not self.logged_in:
            print("Not logged in. Please login to GitHub.")
            time.sleep(2.0)  # Take a nap so GitHub doesn't aggressively throttle us.
            return None

        try:
            repos_formatted_by_categories = {}
            repos = self.ghclient.get_user().get_repos()
            for repo in repos:
                if repo.topics is None or len(repo.topics) == 0:
                    continue
                for topic in repo.topics:
                    if topic not in repos_formatted_by_categories:
                        repos_formatted_by_categories[topic] = {}
                    repos_formatted_by_categories[topic].update(
                        {
                            repo.name: dict(
                                homepage=repo.homepage,
                                html_url=repo.html_url,
                                description=repo.description,
                                readme=self.ghclient.get_user().get_repo(repo.name).get_readme(),
                            )
                        }
                    )
            return repos_formatted_by_categories
        except Exception as e:
            print(f"Error : {e}")
            return None
        
    
