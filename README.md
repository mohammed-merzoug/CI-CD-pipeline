#  E-Commerce Django Application

Application e-commerce professionnelle développée avec Django, avec un pipeline CI/CD complet sur GitLab et une containerisation Docker.

##  Fonctionnalités principales

✨ **Catalogue de produits** - Gestion complète des produits et catégories  
🛒 **Panier d'achat** - Système de panier avec gestion des quantités  
📦 **Gestion des commandes** - Suivi complet des commandes clients  
👤 **Authentification** - Système de comptes utilisateurs avec profils  
🎛️ **Dashboard admin** - Interface d'administration pour gérer le site  
🎨 **Design futuriste** - Interface cyberpunk avec effets néon et glassmorphisme  
📦 **25 produits inclus** - Base de données pré-remplie avec images  
🚀 **CI/CD Pipeline** - Tests et déploiement automatisés via GitLab CI  
🐳 **Docker** - Application containerisée avec Docker & Docker Compose  

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

### 4. Peupler la base de données (recommandé)

```bash
python manage.py populate_db
python manage.py link_images
```

Ces commandes créent **25 produits** répartis en **6 catégories** avec leurs images.

### 5. Créer un superutilisateur (optionnel)

```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur

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

**Identifiants par défaut créés automatiquement :**
- **Username:** `admin`
- **Password:** `admin123`

### Lancer uniquement le conteneur Docker

```bash
docker build -t ecommerce-app .
docker run -d -p 8000:8000 ecommerce-app
```

### ✅ Ce qui est initialisé automatiquement

Le conteneur Docker utilise un script `entrypoint.sh` qui :
- ✅ Applique les migrations de base de données
- ✅ Collecte les fichiers statiques
- ✅ Peuple la base de données avec 25 produits (si vide)
- ✅ Lie automatiquement les images aux produits
- ✅ Crée un superutilisateur par défaut (`admin` / `admin123`)
- ✅ Démarre le serveur Gunicorn

**Note:** Les images des produits (25 fichiers JPG) et le CSS personnalisé sont inclus dans l'image Docker et automatiquement disponibles.

---

##  CI/CD Pipeline GitLab

Le projet utilise un pipeline GitLab CI/CD **portable** basé sur Docker qui fonctionne sur n'importe quel runner GitLab.

### Stages du pipeline

```
test  →  build  →  deploy
```

| Job | Stage | Description |
|-----|-------|-------------|
| `run_tests` | test | Vérifications Django + migrations + tests unitaires |
| `code_quality` | test | Analyse statique du code avec flake8 (erreurs critiques) |
| `build_docker_image` | build | Build de l'image Docker + push vers GitLab Container Registry |
| `deploy_production` | deploy | Déploiement automatique sur `main` (port 8000) |
| `deploy_staging` | deploy | Déploiement automatique sur `develop` (port 8001) |
| `stop_production` | deploy | Arrêt manuel de l'environnement production |
| `stop_staging` | deploy | Arrêt manuel de l'environnement staging |

### Architecture du pipeline

- **Image de base :** `python:3.11-slim` (jobs de test)
- **Build Docker :** `docker:24-dind` avec Docker-in-Docker
- **Deploy :** `docker:24-cli` avec service Docker-in-Docker
- **Portable :** Aucune dépendance à une machine spécifique
- **Automatisé :** Déploiement automatique après succès des tests

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
Design & Interface

L'application utilise un **thème cyberpunk futuriste** avec :

-  **Palette néon** : Cyan, Rose, Violet et Vert néon
-  **Glassmorphisme** : Cartes transparentes avec effet de flou
-  **Animations dynamiques** : Effets de survol, brillance et pulsation
-  **Grille animée** : Fond avec grille cyberpunk en mouvement
-  **Bordures lumineuses** : Contours néon avec effets de lueur
-  **Dégradés** : Boutons et textes avec dégradés cyan-violet
-  **Responsive** : Design adaptatif mobile-first

---

##  Stack technique

| Composant | Technologie | Version |
|-----------|-------------|---------|
| **Backend** | Django | 4.2.7 |
| **Langage** | Python | 3.11 |
| **Base de données** | SQLite | 3.x |
| **Frontend** | Bootstrap | 5.3.0 |
| **Server WSGI** | Gunicorn | 21.2.0 |
| **Conteneurisation** | Docker | 24.x |
| **CI/CD** | GitLab CI | - |
| **Design** | CSS Custom Cyberpunk | - |
| **Fonts** | Google Fonts (Poppins) | - |

---

##  Base de données

**6 catégories de produits :**
- 📱 Électronique (iPhone, MacBook, iPad, AirPods, etc.)
- 👕 Vêtements (T-shirts, jeans, robes, vestes, sneakers)
- 🏠 Maison & Jardin (meubles, lampe, set de jardin)
- ⚽ Sports & Loisirs (haltères, vélo VTT, ballon, tapis de yoga)
- 📚 Livres (Clean Code, Le Petit Prince, L'Art de la Guerre)
- 💄 Beauté & Santé (crème bio, parfum, kit manucure, brosse)

**25 produits avec descriptions, prix, stock et images**

---

##  Architecture du projet

```
ci-cd-pipeline/
  accounts/               # Gestion des utilisateurs
  cart/                   # Panier d'achat
  dashboard/              # Tableau de bord admin
  orders/                 # Gestion des commandes
  shop/                   # Boutique en ligne
    management/
      commands/
        populate_db.py    # Commande pour peupler la DB
        link_images.py    # Commande pour lier les images
  ecommerce_project/      # Configuration Django
  templates/              # Templates HTML
  static/
    css/
      style.css           # Thème cyberpunk futuriste
  media/
    products/             # Images des produits (25 images incluses)
  .gitlab-ci.yml          # Pipeline CI/CD GitLab
  Dockerfile              # Image Docker
  entrypoint.sh           # Script d'initialisation du conteneur
  docker-compose.yml      # Stack Docker Compose (web + nginx)
  .dockerignore           # Exclusions Docker
  requirements.txt        # Dépendances Python
  manage.py               # Commandes Django
  db.sqlite3              # Base de données SQLite
```

---

##  Commandes utiles

| Commande | Description |
|----------|-------------|
| `python manage.py runserver` | Lancer le serveur de développement |
| `python manage.py migrate` | Appliquer les migrations |
| `python manage.py makemigrations` | Créer de nouvelles migrations |
| `python manage.py createsuperuser` | Créer un administrateur |
| `python manage.py populate_db` | Peupler la DB avec 25 produits |
| `python manage.py link_images` | Lier les images aux produits |
| `python manage.py test` | Lancer les tests unitaires |
| `python manage.py collectstatic` | Collecter les fichiers statiques |
| `docker-compose up --build` | Lancer la stack Docker |
| `docker exec -it ecommerce-web bash` | Accéder au shell du conteneur |

---

##  Auteur

Mohammed Merzoug  
GitLab: [@mohammed-merzoug](https://gitlab.com/mohammed-merzoug)

---

##  Licence

Ce projet est développé à des fins éducatives et de démonstration.

### Produits (25)
Tous les produits incluent :
- Images haute qualité dans `media/products/`
- Descriptions détaillées
- Prix réalistes
- Stock disponible
- Certains marqués "mis en avant"

**Exemples :** iPhone 15 Pro, MacBook Air M2, Vélo VTT, Clean Code, Parfum Élégance, etc.

---

##  Résumé rapide

```bash
# Développement local
pip install -r requirements.txt
python manage.py migrate
python manage.py populate_db          # Ajouter les 25 produits
python manage.py createsuperuser      # Optionnel
python manage.py runserver

# Docker
docker-compose up --build

# Tests
python manage.py test --verbosity=2
```

---

** Application e-commerce futuriste complète avec CI/CD ! **

 **Design Cyberpunk** |  **25 Produits** |  **Panier** |  **Command
# Tests
python manage.py test --verbosity=2
```

---

** Application e-commerce complète avec CI/CD et Docker ! **

 **Catalogue** |  **Panier** |  **Commandes** |  **Comptes** |  **Dashboard** |  **CI/CD** |  **Docker**
