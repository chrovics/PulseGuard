# Folosim o versiune mică și rapidă de Linux cu Python 3.11 preinstalat
FROM python:3.11-slim

# Setăm folderul de lucru în container
WORKDIR /app

# Optimizări Python (nu scrie cache, afișează log-urile instant)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copiem doar fișierul de dependențe întâi (pentru viteză la build-urile viitoare)
COPY requirements.txt .

# Instalăm pachetele
RUN pip install --no-cache-dir -r requirements.txt

# Copiem tot restul codului din folderul tău curent în container
COPY . .

# Anunțăm că API-ul va asculta pe portul 8000
EXPOSE 8000
