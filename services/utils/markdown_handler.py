import re
import requests


def download_image(image_url):
    try:
        response = requests.get(image_url, stream=True, allow_redirects=True)
        print(response)
        if response.status_code == 200:
            print("200 OK")
            return response.iter_content(1024)
        else:
            return None
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image : {e}")
        return None


def extract_title_after_dash_first_line(readme_content):
    if not readme_content:
        return None
    # Decode content in UTF-8
    content_str = readme_content.decoded_content.decode("utf-8")
    # Get the first line
    first_line = content_str.split("\n", 1)[0]
    match = re.search(r"- (.+)", first_line)
    # If we have a match, we return the title, otherwise we return the first 
    # line by cleaning the spaces and other special characters at the beginning
    first_line = re.sub(r"^[^a-zA-Z0-9]+", "", first_line)
    return match.group(1) if match else first_line


def extract_first_image(readme_content):
    if not readme_content:
        return None
    content_str = readme_content.decoded_content.decode("utf-8")
    match = re.search(r"!\[.*?\]\((.*?)\)", content_str)
    if match:
        print(match.group(1))
        return download_image(match.group(1))
    else:
        return None


def custom_sort(item):
    # Define key priority
    priority_keys = [
        "goodbarber-custom-features",
        "goodbarber-api-integrations",
        "goodbarber-internal-librairies",
    ]

    if item in priority_keys:
        # Priority higher
        return priority_keys.index(item)
    else:
        # Priority lower
        return len(priority_keys)
