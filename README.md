# goodbarber.github.io

GoodBarber for Developers
=========================



Development
-----------

### Run the site locally
```bash
gem install bundler
bundle install
bundle exec jekyll serve
```

### Install env
```bash
python -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

### Update repos list:
```bash
python update_repos_json.py
```

### Generate static file:
```bash
python generate.py
```

About the code
-----------

Repositories are listed in the `repos.json` file as a map of repository names
to a list of their categories. Invoking the `generate.py` script will update
the `index.html` page with the latest repos by using the `index.mustache` file
as a template.

Repository data is pulled via the GitHub API (e.g., website). To make authenticated
requests and work around the rate-limiting, add an entry for api.github.com to
your ~/.netrc file, preferably with a Personal Access Token from
https://github.com/settings/tokens

    machine api.github.com
      login YourUsername
      password PersonalAccessToken

Images are loaded by convention from the `repo_images/` directory. Ensure the
name is the same as the repo name in the `repos.json` file and has a `.jpg`
extension.