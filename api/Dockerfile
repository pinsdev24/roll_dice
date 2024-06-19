# Utiliser une image officielle Python comme image de base
FROM python:3.9

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le contenu du répertoire actuel dans le répertoire de travail du conteneur
COPY . .

# Exposer le port que l'application Flask utilise
EXPOSE 5000

# Définir la variable d'environnement pour indiquer à Flask l'environnement d'exécution
ENV FLASK_ENV=development

# Indiquer la commande pour démarrer l'application
CMD ["flask", "run", "--host=0.0.0.0"]
