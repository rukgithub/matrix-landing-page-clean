import os
import requests
import base64
import time

# Konfiguration
GITHUB_USERNAME = "rukgithub"
REPO_NAME = "matrix-landing-page-clean"
IMAGE_FOLDER = r"C:\Users\ruk\Downloads\billeder"

# Hent GitHub-token fra miljøvariabler
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GitHub token mangler! Sæt 'GITHUB_TOKEN' som en miljøvariabel.")


def get_image_files(folder):
    """Returner en liste over billedfiler i den angivne mappe."""
    supported_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
    try:
        return [f for f in os.listdir(folder) if f.lower().endswith(supported_extensions)]
    except Exception as e:
        print(f"Error reading image folder: {e}")
        return []


def get_file_sha(path):
    """Hent SHA for en eksisterende fil."""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('sha')
    return None


def upload_file_to_repo(path, content, is_binary=False, message="Add/Update file"):
    """Upload eller opdater en fil i GitHub repository."""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Konvertér content til Base64
    if not is_binary:
        content = content.encode('utf-8')
    encoded_content = base64.b64encode(content).decode('utf-8')

    # Tjek om filen eksisterer og få SHA
    sha = get_file_sha(path)

    # Forbered data til API request
    data = {
        "message": message,
        "content": encoded_content
    }
    if sha:
        data["sha"] = sha

    # Upload filen
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        print(f"✓ Success: '{path}' uploaded")
        return True
    else:
        print(f"✗ Error uploading '{path}': {response.json()}")
        return False


def upload_image_to_repo(image_path):
    """Upload et billede til GitHub repository."""
    try:
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        image_name = os.path.basename(image_path)
        return upload_file_to_repo(
            f"images/{image_name}",
            content,
            is_binary=True,
            message=f"Add/Update {image_name}"
        )
    except Exception as e:
        print(f"Error uploading {image_path}: {e}")
        return False


def generate_index_html(image_files):
    """Generer index.html med Matrix tema."""
    html_content = """
    <!DOCTYPE html>
    <html lang="da">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Matrix Image Gallery</title>
        <style>
            body { 
                background-color: #000; 
                color: #0f0; 
                font-family: 'Courier New', Courier, monospace; 
                margin: 0; 
                padding: 0;
                min-height: 100vh;
            }
            .container { 
                display: flex; 
                flex-wrap: wrap; 
                justify-content: center; 
                padding: 20px; 
                gap: 20px;
            }
            .image-box { 
                background: rgba(0, 255, 0, 0.1);
                border: 2px solid #0f0; 
                padding: 10px;
                transition: all 0.3s ease;
                max-width: 300px;
            }
            .image-box img { 
                width: 100%;
                height: auto; 
                display: block;
            }
            .image-box:hover { 
                transform: scale(1.05);
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            }
            h1 { 
                text-align: center; 
                padding: 20px;
                text-shadow: 0 0 10px #0f0;
            }
        </style>
    </head>
    <body>
        <h1>Matrix Image Gallery</h1>
        <div class="container">
    """

    # Tilføj billeder
    for image in image_files:
        html_content += f"""
            <div class="image-box">
                <img src="images/{image}" alt="{image}" loading="lazy">
            </div>
        """

    # Afslut HTML
    html_content += """
        </div>
    </body>
    </html>
    """

    return html_content


def main():
    print("Starting Matrix Landing Page Generator...")

    # Hent billedfiler
    print("\nScanning for images...")
    images = get_image_files(IMAGE_FOLDER)
    if not images:
        print("✗ Error: No images found in the specified folder!")
        exit(1)
    print(f"✓ Found {len(images)} images")

    # Upload billeder
    print("\nUploading images...")
    successful_uploads = 0
    for image in images:
        image_path = os.path.join(IMAGE_FOLDER, image)
        if upload_image_to_repo(image_path):
            successful_uploads += 1
        time.sleep(0.5)  # Lille pause mellem uploads

    print(f"\n✓ Successfully uploaded {successful_uploads} of {len(images)} images")

    # Generer og upload index.html
    print("\nGenerating and uploading index.html...")
    index_html = generate_index_html(images)
    if upload_file_to_repo("index.html", index_html, message="Update index.html with Matrix theme"):
        print("\n✓ Successfully completed all tasks!")
        print(f"\nYour Matrix Landing Page should now be available at:")
        print(f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/")
    else:
        print("\n✗ Error: Failed to upload index.html")


if __name__ == "__main__":
    main()