@echo off
REM Création de l'environnement virtuel si besoin
if not exist ".venv\" (
    echo 🔧 Création de l'environnement virtuel...
    python -m venv .venv
)

REM Activation de l'environnement
call .venv\Scripts\activate.bat

REM Installation des dépendances
echo 📦 Installation des dépendances...
pip install -r requirements.txt

REM Lancement du projet
echo 🚀 Lancement de main.py...
python main.py

REM Pause pour garder la console ouverte
pause