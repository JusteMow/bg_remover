# Pipelines de Background Remover

#pipeline #ui #processing #background-removal

**Classes impliquées :**
- [App](/src/ui.py)
- [ImageProcessor](/src/processor.py)
- [SliderWithEntry](/src/sliderWithEntry.py)

## Pipeline de Traitement d'Image

### Traitement d'une Image Unique
**Déclencheur :** `App.process_image()`

```pipeline
App.process_image()
├─> vérifier si input_image existe
├─> si auto_update est activé:
│   └─> update_preview()
│       ├─> display_preview(input_canvas, input_image)
│       └─> display_preview(output_canvas, output_image)
└─> sinon:
    ├─> output_image = ImageProcessor.process_image()
    │   ├─> sélectionner le modèle (u2net, u2netp, silueta)
    │   ├─> configurer le device (GPU/CPU)
    │   └─> appeler rembg.remove() avec les paramètres
    ├─> display_preview(output_canvas, output_image)
    └─> update_status("Image traitée avec succès", "green")
```

**Paramètres de traitement :**
- Modèle de segmentation (u2net, u2netp, silueta)
- Alpha Matting (activé/désactivé)
- Seuils avant/arrière-plan
- Taille d'érosion
- Utilisation du GPU

## Pipeline de Traitement par Lot

### Traitement d'un Dossier
**Déclencheur :** `App.process_whole_folder()`

```pipeline
App.process_whole_folder()
├─> select_folder("input_files", "Sélectionner le dossier d'entrée")
├─> select_folder("output_files", "Sélectionner le dossier de sortie")
└─> ImageProcessor.process_whole_folder()
    ├─> créer le dossier de sortie
    ├─> pour chaque fichier image:
    │   ├─> ouvrir l'image
    │   ├─> process_image() avec les paramètres par défaut
    │   ├─> générer un nom de fichier unique
    │   └─> sauvegarder l'image traitée
    └─> update_status("Traitement terminé", "green")
```

## Pipeline de l'Interface Utilisateur

### Gestion des Paramètres
**Déclencheur :** Modification des contrôles UI

```pipeline
App.build_interface()
├─> Création des contrôles
│   ├─> SliderWithEntry pour les seuils
│   ├─> Checkbox pour auto_update
│   ├─> Checkbox pour alpha_matting
│   ├─> Checkbox pour GPU
│   └─> Radio buttons pour le modèle
└─> Binding des événements
    ├─> check_auto_update() sur modification des paramètres
    └─> update_preview() si auto_update est activé
```

### Gestion des Fichiers
**Déclencheur :** Actions utilisateur sur les boutons de fichier

```pipeline
App.select_input_file()
├─> filedialog.askopenfilename()
├─> charger l'image
└─> display_preview(input_canvas, input_image)

App.select_output_file()
├─> filedialog.asksaveasfilename()
└─> sauvegarder output_image
```

## Tags
#background-removal #ui #processing #pipeline #image-processing 