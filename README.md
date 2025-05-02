Pour travailler avec Django de façon officielle sur votre système, vous devez fait au préalable quelques installations:

1- Commencer par vérifier si python est installer et fonctionne correctement sur votre système: CMD(python --version)
2- Vérifier l'installation de pip avec la commande: pip --version
3- installer Django dans un environnement virtuelle (Toujours recommandée ), pour cela:
	
	- créer l'environnement avec: python -m venv env
	- activer l'environnement avec: env\Scripts\activate
	- Passer à l'installation de Django: pip install Django
	- Vérifier l’installation: django-admin --version

4- Créer un nouveau projet Django: 
		- django-admin startproject mon_projet
		- cd mon_projet
		- lancer le projet : python manage.py runserver
5- Créer une application Django
	- Assurez- vous d'etre dans le dossier mon_projet
	- taper la commande : python manage.py startapp my_app 
	
6- Enregistrer l’application dans le projet
	- Ouvre le fichier mon_projet/settings.py et ajoute 'my_app', dans la liste INSTALLED_APPS
	INSTALLED_APPS = [
    	'django.contrib.admin',
    	'django.contrib.auth',
    	...
    	'my_app',
	]
7- Créer une première vue
	Dans my_app/views.py, ajoute :
	la fonction accueil avec:
		
		from django.http import HttpResponse

		def accueil(request):
    			return HttpResponse("Bienvenue dans ma première application Django !")

8- Créer un fichier urls.py dans ton app (si pas encore présent)
Dans my_app/urls.py :
	
	from django.urls import path
	from . import views

	urlpatterns = [
    		path('', views.accueil, name='accueil'),
	]
9- Inclure les URLs de l’app dans le projet principal
	Dans mon_projet/urls.py, ajoute :
	
	urlpatterns = [
    		path('admin/', admin.site.urls),
    		path('', include('ma_premiere_app.urls')),  # <- ceci
	]

Vous pouvez par la suite relancer le serveur


Passons à l'autentification d'un utilisateur ou d'un superUser

Django, de base, fournit un système d’authentification intégré (gestion des utilisateurs, connexion, déconnexion, mots de passe, etc.).

Voici comment ajouter un système d’authentification complet à notre projet my_app.

Configuration importante dans settings.py avant migrate
1. Configuration de la base de données
Par défaut, Django utilise SQLite :
 Si tu veux utiliser MySQL, PostgreSQL, etc., il faut modifier cela. Exemple pour MYSQL:
	- Installer le connecteur MySQL pour Python: pip install mysqlclient
	- si ça te renvoie des erreurs: pip install mysqlclient‑1.4.6‑cp39‑cp39‑win_amd64.whl (selon ta version)
2- Créer une base de données MySQL pour my_app
3- Configurer settings.py
	Dans mon_projet/settings.py, remplace la section DATABASES par :
	
	DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_app',
        'USER': 'nom_utilisateur',
        'PASSWORD': 'ton_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

Configurer la Langue et fuseau horaire
Adapte selon ta région :

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'  # ou autre

4- Appliquer les migrations
Une fois configuré, exécute :
python manage.py makemigrations
python manage.py migrate

5- Crée un superutilisateur pour accéder à l'admin au besoin :

python manage.py createsuperuser

Puis :

python manage.py runserver

Accède à http://127.0.0.1:8000/admin
	
6- Dans votre application my_app, créer un dossier templates avec les fichiers:
		
	- login.html
    	- register.html
	- home.html

7- créer un dossier templates à la racine de votre projet

mon_projet/
│
├── manage.py
├── mon_projet/                ← dossier du projet (nom identique à la racine)
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── my_app/                     ← app pour gérer l’authentification
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/
│       └── my_app/
│           ├── login.html
│           ├── register.html
│           └── home.html
│
├── static/                    ← fichiers CSS/JS/images
│
└── templates/                 ← templates globaux si nécessaire
    └── base.html


Contenue de pages:

Login.html

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Connexion</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
  <div class="container d-flex align-items-center justify-content-center" style="height: 100vh;">
    <div class="card p-4 shadow" style="width: 100%; max-width: 400px;">
      <h4 class="text-center mb-4">Connexion</h4>
      <form method="POST">
        {% csrf_token %}
        <div class="mb-3">
          <label for="username" class="form-label">Nom d'utilisateur</label>
          <input type="text" class="form-control" id="username" name="username" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Mot de passe</label>
          <input type="password" class="form-control" id="password" name="password" required>
        </div>
        <button type="submit" class="btn btn-primary w-100">Se connecter</button>
      </form>
      <div class="mt-3 text-center">
        <a href="{% url 'register' %}">Créer un compte</a>
      </div>
      {% if messages %}
        <div class="mt-3 alert alert-danger">
          {% for message in messages %}
            {{ message }}
          {% endfor %}
        </div>
      {% endif %}
    </div>
  </div>
</body>
</html>


Register.html

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Inscription</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
  <div class="container d-flex align-items-center justify-content-center" style="height: 100vh;">
    <div class="card p-4 shadow" style="width: 100%; max-width: 500px;">
      <h4 class="text-center mb-4">Créer un compte</h4>
      <form method="POST">
        {% csrf_token %}
        <div class="mb-3">
          <label for="username" class="form-label">Nom d'utilisateur</label>
          <input type="text" class="form-control" id="username" name="username" required>
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Adresse e-mail</label>
          <input type="email" class="form-control" id="email" name="email" required>
        </div>
        <div class="mb-3">
          <label for="password1" class="form-label">Mot de passe</label>
          <input type="password" class="form-control" id="password1" name="password1" required>
        </div>
        <div class="mb-3">
          <label for="password2" class="form-label">Confirmer le mot de passe</label>
          <input type="password" class="form-control" id="password2" name="password2" required>
        </div>
        <button type="submit" class="btn btn-success w-100">S'inscrire</button>
      </form>
      <div class="mt-3 text-center">
        <a href="{% url 'login' %}">Déjà un compte ? Connectez-vous</a>
      </div>
      {% if messages %}
        <div class="mt-3 alert alert-danger">
          {% for message in messages %}
            {{ message }}
          {% endfor %}
        </div>
      {% endif %}
    </div>
  </div>
</body>
</html>


Dashboard.html

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container mt-5 text-center">
        <h1>Bienvenue, {{ request.user.username }} !</h1>
        <a href="{% url 'logout' %}" class="btn btn-danger mt-3">Se déconnecter</a>
    </div>
</body>
</html>



## Dans views.py

Ajouter les fonctions pour register, login, etc:

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse e-mail est déjà utilisée.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Compte créé avec succès. Connectez-vous.")
        return redirect('login')

    return render(request, 'my_app/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # ou la page après connexion
        else:
            messages.error(request, "Identifiants invalides.")
            return redirect('my_app/login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

Modifier le urls.py

from django.urls import path
from . import views
from .views import register_view, login_view, logout_view
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

urlpatterns = [
    # path('', views.accueil, name='accueil'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Page d'accueil protégée
    path('', login_required(lambda request: render(request, 'my_app/dashboard.html')), name='home'),
]



Django, par défaut, redirige les utilisateurs non connectés vers /accounts/login/, qui n’existe pas si on ne l’as pas définie.

Définis ta propre URL de login dans settings.py
Ajoute cette ligne dans ton settings.py :

LOGIN_URL = '/login/'  
LOGIN_REDIRECT_URL = '/'

