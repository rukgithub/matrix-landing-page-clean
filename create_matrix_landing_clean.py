import os
import requests
from jinja2 import Template

# Konfiguration
GITHUB_USERNAME = "rukgithub"
REPO_NAME = "matrix-landing-page-clean"  # Navnet på dit nye repository
IMAGE_FOLDER = r"C:\Users\ruk\Downloads\billeder"  # Opdater til din billedmappe

# Hent GitHub-token fra miljøvariabler
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Sørg for, at tokenet er sat som en miljøvariabel

if not GITHUB_TOKEN:
    raise ValueError("GitHub token mangler! Sæt 'GITHUB_TOKEN' som en miljøvariabel.")

def get_image_files(folder):
    """Returner en liste over billedfiler i den angivne mappe."""
    supported_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
    return [f for f in os.listdir(folder) if f.lower().endswith(supported_extensions)]

def create_github_repo():
    """Opret et nyt GitHub repository."""
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": REPO_NAME,
        "description": "A responsive Matrix-themed landing page displaying images.",
        "homepage": f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/",
        "private": False,
        "has_pages": True
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Repository '{REPO_NAME}' oprettet succesfuldt.")
    elif response.status_code == 422:
        print("Repositoryet eksisterer allerede på GitHub.")
    else:
        print("Fejl ved oprettelse af repository:", response.json())
        exit(1)

def upload_file_to_repo(path, content, message="Add file"):
    """Upload en fil til GitHub repository."""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": message,
        "content": content.encode('utf-8').decode('utf-8'),
    }

    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        print(f"Uploaded '{path}' succesfuldt.")
    else:
        print(f"Fejl ved upload af '{path}':", response.json())

def generate_index_html(image_files):
    """Generer index.html med Matrix tema."""
    template = Template("""
    <!DOCTYPE html>
    <html lang="da">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Matrix Landing Page</title>
        <style>
            body { background-color: #000; color: #0f0; font-family: 'Courier New', Courier, monospace; margin: 0; padding: 0; }
            .container { display: flex; flex-wrap: wrap; justify-content: center; padding: 20px; }
            .image-box { margin: 10px; border: 2px solid #0f0; padding: 5px; transition: transform 0.2s; }
            .image-box img { max-width: 100%; height: auto; display: block; }
            .image-box:hover { transform: scale(1.05); }
        </style>
    </head>
    <body>
        <h1 style="text-align:center; padding:20px;">Matrix Themed Image Gallery</h1>
        <div class="container">
            {% for image in images %}
            <div class="image-box">
                <img src="images/{{ image }}" alt="{{ image }}">
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """)
    return template.render(images=image_files)

def main():
    # Opret repository
    create_github_repo()

    # Hent billedfiler
    images = get_image_files(IMAGE_FOLDER)
    if not images:
        print("Ingen billedfiler fundet i mappen.")
        exit(1)

    # Generer index.html
    index_html = generate_index_html(images)
    upload_file_to_repo("index.html", index_html, message="Add index.html")

if __name__ == "__main__":
    main()
