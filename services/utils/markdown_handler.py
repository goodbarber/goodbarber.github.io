import re
import requests


def download_image(image_url):
    try:
        response = requests.get(image_url, stream=True, allow_redirects=True)
        if response.status_code == 200:
            print("200 OK")
            return response.iter_content(1024)
        else:
            return None
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image : {e}")
        return None


def extract_text_after_dash_first_line(readme_content):
    if not readme_content:
        return None
    content_str = readme_content.decoded_content.decode(
        "utf-8"
    )  # Décode le contenu en UTF-8
    first_line = content_str.split("\n", 1)[0]  # Récupère la première ligne
    match = re.search(r"- (.+)", first_line)
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
