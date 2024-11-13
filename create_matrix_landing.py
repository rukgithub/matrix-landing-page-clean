import os
import requests
import base64
from jinja2 import Template

# --- Konfiguration ---
GITHUB_USERNAME = "rukgithub"  # Din GitHub brugernavn
REPO_NAME = "matrix-landing-page"  # Navn på det nye repository
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Henter tokenet fra en miljøvariabel
IMAGE_FOLDER = r"C:\Users\ruk\Downloads\billeder"  # Sti til din billedmappe

# --- Funktioner ---

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
    # Tjek om filen allerede eksisterer for at få sha
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json()['sha']
    else:
        sha = None

    data = {
        "message": message,
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
    }
    if sha:
        data["sha"] = sha

    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        print(f"Uploaded '{path}' succesfuldt.")
    else:
        print(f"Fejl ved upload af '{path}':", response.json())

def upload_image_to_repo(image_path):
    """Upload en enkelt billedfil til GitHub repository."""
    with open(image_path, "rb") as img_file:
        content = base64.b64encode(img_file.read()).decode('utf-8')
    # Filsti i repository
    repo_path = f"images/{os.path.basename(image_path)}"
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{repo_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    # Tjek om filen allerede eksisterer for at få sha
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json()['sha']
    else:
        sha = None

    data = {
        "message": f"Add {repo_path}",
        "content": content,
    }
    if sha:
        data["sha"] = sha

    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        print(f"Uploaded '{repo_path}' succesfuldt.")
    else:
        print(f"Fejl ved upload af '{repo_path}':", response.json())

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
            body {
                background-color: #000;
                color: #0f0;
                font-family: 'Courier New', Courier, monospace;
                margin: 0;
                padding: 0;
            }
            .container {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                padding: 20px;
            }
            .image-box {
                margin: 10px;
                border: 2px solid #0f0;
                padding: 5px;
                transition: transform 0.2s;
            }
            .image-box img {
                max-width: 100%;
                height: auto;
                display: block;
            }
            .image-box:hover {
                transform: scale(1.05);
            }
            @media (max-width: 600px) {
                .image-box {
                    width: 100%;
                }
            }
            @media (min-width: 601px) and (max-width: 1200px) {
                .image-box {
                    width: 45%;
                }
            }
            @media (min-width: 1201px) {
                .image-box {
                    width: 30%;
                }
            }
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

    # Upload billeder
    for image in images:
        image_path = os.path.join(IMAGE_FOLDER, image)
        upload_image_to_repo(image_path)

    print(f"Landing page er klar på https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/")

if __name__ == "__main__":
    main()
