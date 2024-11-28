# Immagine base
FROM python:3.11

# Impostazioni di lavoro
WORKDIR /app

# Copia i file necessari
COPY . /app

# Aggiorna pip
RUN pip install --upgrade pip

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

RUN ngrok http --domain=$DOMINIO $FLASK_HOST:$FLASK_PORT

# Espone la porta 5000
EXPOSE $FLASK_PORT

# Avvia l'app Flask
CMD ["python", "main.py"]

