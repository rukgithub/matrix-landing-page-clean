from flask import Flask, render_template_string, send_from_directory
import os

app = Flask(__name__)

# Sti til mappen med billederne
BILLEDEMAPPE = r"C:\Users\ruk\Downloads\billeder"

# Template for UI med klikbare billeder
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="da">
<head>
    <meta charset="UTF-8">
    <title>Billedgalleri</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background-color: #f0f0f0; }
        .gallery { display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; }
        .gallery img { 
            width: 200px; height: 200px; object-fit: cover;
            border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
            cursor: pointer;
        }
        .gallery a { text-decoration: none; color: inherit; }
    </style>
</head>
<body>
    <h1>Billedgalleri</h1>
    <div class="gallery">
        {% for billede in billeder %}
        <a href="{{ url_for('vis_billede', filnavn=billede) }}" target="_blank">
            <img src="{{ url_for('vis_billede', filnavn=billede) }}" alt="Billede">
        </a>
        {% endfor %}
    </div>
</body>
</html>
"""

# Hjemmeside-rute
@app.route('/')
def galleri():
    # Filtrerer for billedfiler i den angivne mappe
    billeder = [fil for fil in os.listdir(BILLEDEMAPPE) if fil.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    return render_template_string(HTML_TEMPLATE, billeder=billeder)

# Rute til at vise et billedegit --version
@app.route('/billeder/<filnavn>')
def vis_billede(filnavn):
    return send_from_directory(BILLEDEMAPPE, filnavn)

if __name__ == '__main__':
    app.run(debug=True)
