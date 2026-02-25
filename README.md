#  E-Commerce Django Application

Application e-commerce professionnelle développée avec Django, avec un pipeline CI/CD complet sur GitLab et une containerisation Docker.

##  Fonctionnalités principales

 **Catalogue de produits** - Gestion complète des produits et catégories  
 **Panier d'achat** - Système de panier avec gestion des quantités  
 **Gestion des commandes** - Suivi complet des commandes clients  
 **Authentification** - Système de comptes utilisateurs avec profils  
 **Dashboard admin** - Interface d'administration pour gérer le site  
 **Responsive design** - Interface moderne avec Bootstrap 5  
 **CI/CD Pipeline** - Tests et déploiement automatisés via GitLab CI  
 **Docker** - Application containerisée avec Docker & Docker Compose  

---

##  Démarrage rapide (développement local)

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Activer l'environnement virtuel

**Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Appliquer les migrations

```bash
python manage.py migrate
```

### 4. Créer un superutilisateur (optionnel)

```bash
python manage.py createsuperuser
```

### 5. Lancer le serveur

```bash
python manage.py runserver
```

- **Site web :** http://127.0.0.1:8000
- **Administration Django :** http://127.0.0.1:8000/admin
- **Accès réseau local (téléphone) :** http://192.168.11.100:8000

---

##  Démarrage avec Docker

### Lancer avec Docker Compose

```bash
docker-compose up --build
```

- **Application :** http://localhost:8000
- **Via Nginx :** http://localhost:80

### Lancer uniquement le conteneur Docker

```bash
docker build -t ecommerce-app .
docker run -d -p 8000:8000 ecommerce-app
```

---

##  CI/CD Pipeline GitLab

Le projet utilise un pipeline GitLab CI/CD automatisé tournant sur un **runner Windows local** (MOCRO).

### Stages du pipeline

```
dependencies  test  build  deploy
```

| Job | Stage | Description |
|-----|-------|-------------|
| `install_dependencies` | dependencies | Crée le venv et installe les paquets |
| `run_tests` | test | Vérifications Django + 31 tests unitaires |
| `code_quality` | test | Analyse statique du code avec flake8 |
| `build_docker_image` | build | Build et push vers le GitLab Container Registry |
| `production_deploy` | deploy | Déploiement automatique sur `main` |
| `staging_deploy` | deploy | Déploiement automatique sur `develop` |

### Configuration du runner

- **Runner :** MOCRO (Windows, shell executor PowerShell)
- **Tag :** `windows`
- **Fichier de config :** `C:\GitLab-Runner\config.toml`

### Déclencher le pipeline

Tout push sur `main` déclenche automatiquement le pipeline complet :

```bash
git push origin main
```

### Variables CI/CD (injectées automatiquement par GitLab)

| Variable | Description |
|----------|-------------|
| `CI_REGISTRY` | URL du registre GitLab |
| `CI_REGISTRY_USER` | Utilisateur du registre |
| `CI_REGISTRY_PASSWORD` | Mot de passe du registre |
| `CI_REGISTRY_IMAGE` | Image complète avec tag |

---

##  Tests

31 tests unitaires couvrant tous les modules :

```bash
python manage.py test --verbosity=2
```

| Module | Classe de test | Nb tests |
|--------|----------------|----------|
| `shop` | CategoryModelTest, ProductModelTest, ShopViewTest | 9 |
| `accounts` | UserRegistrationTest | 7 |
| `cart` | CartViewTest | 4 |
| `orders` | OrderModelTest, OrderViewTest | 6 |
| `dashboard` | DashboardAccessTest | 5 |

---

##  Modules de l'application

###  Shop (Boutique)
- Catalogue de produits et catégories
- Pages produits détaillées
- Pages statiques (À propos, Contact, FAQ, etc.)

###  Accounts (Comptes utilisateurs)
- Inscription et connexion
- Profils et adresses utilisateurs
- Réinitialisation de mot de passe

###  Cart (Panier)
- Ajout/suppression de produits
- Modification des quantités
- Calcul automatique des totaux

###  Orders (Commandes)
- Création et suivi des commandes
- Historique et statut des commandes

###  Dashboard (Tableau de bord admin)
- CRUD produits et catégories
- Liste commandes et utilisateurs
- Accès réservé aux administrateurs

---

##  Stack technique

| Composant | Technologie | Version |
|-----------|-------------|---------|
| **Backend** | Django | 4.2.7 |
| **Langage** | Python | 3.11 |
| **Base de données** | SQLite | 3.x |
| **Frontend** | Bootstrap | 5.3.0 |
| **Serveur WSGI** | Gunicorn | 21.2.0 |
| **Proxy inverse** | Nginx | latest |
| **Conteneurisation** | Docker | - |
| **CI/CD** | GitLab CI | - |

---

##  Architecture du projet

```
ci-cd-pipeline/
  accounts/               # Gestion des utilisateurs
  cart/                   # Panier d achat
  dashboard/              # Tableau de bord admin
  orders/                 # Gestion des commandes
  shop/                   # Boutique en ligne
  ecommerce_project/      # Configuration Django
  templates/              # Templates HTML
  static/                 # Fichiers statiques
  media/                  # Fichiers uploades
  .gitlab-ci.yml          # Pipeline CI/CD GitLab
  Dockerfile              # Image Docker
  docker-compose.yml      # Stack Docker Compose (web + nginx)
  .dockerignore           # Exclusions Docker
  deploy.ps1              # Script de deploiement PowerShell
  requirements.txt        # Dependances Python
  manage.py               # Commandes Django
  db.sqlite3              # Base de donnees SQLite
```

---

##  Commandes utiles

| Commande | Description |
|----------|-------------|
| `python manage.py runserver` | Lancer le serveur de développement |
| `python manage.py migrate` | Appliquer les migrations |
| `python manage.py makemigrations` | Créer de nouvelles migrations |
| `python manage.py createsuperuser` | Créer un administrateur |
| `python manage.py test` | Lancer les tests unitaires |
| `python manage.py collectstatic` | Collecter les fichiers statiques |
| `docker-compose up --build` | Lancer la stack Docker |

---

##  Sécurité

**Implémenté :**
-  Protection CSRF sur tous les formulaires
-  Authentification requise pour les zones sensibles
-  Validation des formulaires côté serveur
-  Gestion sécurisée des mots de passe (hashing)
-  Séparation des permissions admin/utilisateur

**À configurer pour la production :**
-  `DEBUG = False`
-  `ALLOWED_HOSTS` restreint aux domaines autorisés
-  Migrer vers PostgreSQL ou MySQL
-  Activer HTTPS / TLS
-  Utiliser des variables d environnement pour les secrets

---

##  Résumé rapide

```bash
# Développement local
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Docker
docker-compose up --build

# Tests
python manage.py test --verbosity=2
```

---

** Application e-commerce complète avec CI/CD et Docker ! **

 **Catalogue** |  **Panier** |  **Commandes** |  **Comptes** |  **Dashboard** |  **CI/CD** |  **Docker**
