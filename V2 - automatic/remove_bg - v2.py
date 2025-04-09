from rembg import remove
from rembg.session_factory import new_session
from PIL import Image
import os

# Charger un modèle spécifique
session_u2net = new_session("u2net")  # Autres options : "u2netp", "silueta"
session_u2netp = new_session("u2netp")  
session_silueta = new_session("silueta")

# Définir les dossiers d'entrée et de sortie
root_dir = os.getcwd()  # Répertoire courant
input_dir = os.path.join(root_dir, "Input_files")
output_dir = os.path.join(root_dir, "Output_files")

# Créer le dossier de sortie s'il n'existe pas
os.makedirs(output_dir, exist_ok=True)

# Itérer sur tous les fichiers du dossier Input_files
for file_name in os.listdir(input_dir):
    input_path = os.path.join(input_dir, file_name)

    # Vérifier si le fichier est une image (vous pouvez ajouter d'autres extensions si nécessaire)
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        try:
            # Charger l'image
            inp = Image.open(input_path)

            # Définir le chemin de sortie
            output_path = os.path.join(output_dir, os.path.splitext(file_name)[0] + "_no_bg")

            # Utiliser les sessions spécifiques pour chaque modèle
            output_u2net = remove(inp, session=session_u2net)
            output_u2netp = remove(inp, session=session_u2netp)
            output_silueta = remove(inp, session=session_silueta)

            # Sauvegarder chaque résultat
            output_u2net.save(output_path + "_u2net.png")
            output_u2netp.save(output_path + "_u2netp.png")
            output_silueta.save(output_path + "_silueta.png")

            print(f"Traitement terminé pour : {file_name}")
        except Exception as e:
            print(f"Erreur lors du traitement de {file_name}: {e}")

print("Traitement terminé pour tous les fichiers.")
