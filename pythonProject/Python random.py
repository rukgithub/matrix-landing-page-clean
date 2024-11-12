import requests
import os
import time

# URL til Replicate API for at lave forudsigelser
url = "https://api.replicate.com/v1/predictions"

# Dine headers med den nye API-nøgle
headers = {
    "Authorization": "Token r8_CzhPy1z7xh0PphFOwDKLWHqro28pzth2V2lw7",  # Erstat med din nye API-nøgle
    "Content-Type": "application/json"
}

# Opdateret version-ID fra Replicate
version_id = "j36hzp13vdrme0ck1148gp9pyc"  # Erstat med det korrekte version-ID

# Opsætning af input-parametre til API-kaldet
data = {
    "version": version_id,
    "input": {
        "prompt": "supermodel in a fashion photoshoot",  # Juster prompten efter dine behov
        "num_outputs": 1,  # Antal billeder
        "guidance_scale": 3.5,
        "num_inference_steps": 28,
        "output_format": "webp",  # Kan ændres til 'png' hvis ønsket
        "output_quality": 90,
        "trigger_word": "supermodel",
        # Tilføj andre parametre efter behov
    }
}

# Sender API-kaldet til Replicate
response = requests.post(url, headers=headers, json=data)

# Tjekker om kaldet lykkedes
if response.status_code == 201:
    prediction = response.json()
    prediction_id = prediction['id']
    status = prediction['status']
    print(f"Prediction ID: {prediction_id}")
    print(f"Status: {status}")

    # Polling for prediction status
    while status != "succeeded" and status != "failed":
        time.sleep(2)  # Vent 2 sekunder før næste tjek
        status_response = requests.get(f"https://api.replicate.com/v1/predictions/{prediction_id}", headers=headers)
        if status_response.status_code == 200:
            prediction = status_response.json()
            status = prediction['status']
            print(f"Status: {status}")
        else:
            print("Fejl ved hentning af prediction status:", status_response.json())
            break

    if status == "succeeded":
        output = prediction['output']
        if isinstance(output, list):
            image_url = output[0]  # Hent første billede hvis flere er genereret
        else:
            image_url = output

        # Stien hvor billedet skal gemmes
        save_directory = r"C:\Users\ruk\Downloads\hhhhh\jjj"
        os.makedirs(save_directory, exist_ok=True)  # Opretter mappen, hvis den ikke eksisterer
        save_path = os.path.join(save_directory, "generated_image.webp")  # Ændr filtypen hvis nødvendigt

        # Henter og gemmer billedet
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(image_response.content)
            print(f"Billede gemt til {save_path}")
        else:
            print("Fejl ved hentning af billedet:", image_response.status_code)
    else:
        print("Prediction mislykkedes:", prediction)
else:
    print("Fejl:", response.json())
