import tkinter as tk
from tkinter import filedialog, Canvas, Label, Button, Radiobutton, IntVar, Scale, Frame, Checkbutton, BooleanVar
from .processor import ImageProcessor
from PIL import Image, ImageTk, ImageDraw
import os
import sys
from .sliderWithEntry import SliderWithEntry


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Background Remover")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2b2b2b")  # Dark mode

        # Initialiser le processeur d'images
        self.processor = ImageProcessor()

        # Variables globales
        self.input_file = None
        self.output_file = None
        self.input_image = None
        self.output_image = None
        self.selected_model = IntVar(value=1)  # 1 = u2net, 2 = u2netp, 3 = silueta
        self.foreground_threshold = 240
        self.background_threshold = 10
        self.erode_size = 10
        self.auto_update = BooleanVar(value=True)
        self.use_alpha_matting = BooleanVar(value=False)
        self.use_gpu = BooleanVar(value=True)
        self.show_original = BooleanVar(value=False)
        self.status_label = None

        # Chemins par défaut
        self.root_dir = os.getcwd()
        self.output_dir = os.path.join(self.root_dir, "output_files")

        # Construire l'interface
        self.build_interface()

        # Ajouter le binding pour recharger l'application
        self.root.bind("r", lambda _: self.reload_app())

    def build_interface(self):
        # Layout principal : 2 colonnes (Preview + Parameters)
        main_frame = Frame(self.root, bg="#2b2b2b")
        main_frame.pack(fill="both", expand=True)


        # Colonne Preview (redimensionnable)
        # Colonne Preview (redimensionnable)
        preview_frame = Frame(main_frame, bg="#2b2b2b")
        preview_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)  # La colonne Preview peut s'étendre
        main_frame.grid_rowconfigure(0, weight=1)  # Permet à la colonne Preview de s'étendre verticalement


        # Frame pour le titre et la case à cocher
        title_frame = Frame(preview_frame, bg="#2b2b2b")
        title_frame.pack(fill="x", pady=10)

        # Titre à gauche
        Label(title_frame, text="Local_BG_REM by Juste Mow ", bg="#2b2b2b", fg="white", font=("Arial", 16, "bold")).pack(side="left", padx=10)

        # Case à cocher à droite
        Checkbutton(
            title_frame,
            text="Show Original",
            variable=self.show_original,
            command=self.toggle_preview,
            bg="#2b2b2b",
            fg="white",
            selectcolor="#2b2b2b"
        ).pack(side="right", padx=10)

        # Canvas pour l'aperçu
        self.input_canvas = Canvas(preview_frame, width=600, height=600, bg="black")
        self.input_canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # Resier Canvas 
        self.input_canvas.bind("<Configure>", self.on_resize)

        # Colonne Parameters (fixe à 300 pixels)
        param_frame = Frame(main_frame, bg="#2b2b2b", width=300)
        param_frame.grid(row=0, column=1, sticky="nsew")
        param_frame.grid_propagate(False)
        main_frame.grid_columnconfigure(1, minsize=300)  # Fixe la 

        # Bouton : "Select Input File"
        Button(param_frame, text="Select Input File", command=self.select_input_file, bg="#444", fg="white").pack(pady=10, fill="x")

        # Case à cocher : CPU /
        Checkbutton(param_frame, text="Use GPU", variable=self.use_gpu, bg="#2b2b2b", fg="white", selectcolor="#2b2b2b").pack(pady=10)

        # Case à cocher : "Auto Update"
        Checkbutton(param_frame, text="Auto Update", variable=self.auto_update, bg="#2b2b2b", fg="white", selectcolor="#2b2b2b").pack(pady=10)

        # Boutons radio pour les modèles
        Radiobutton(param_frame, text="U2Net", variable=self.selected_model, value=1, command=self.check_auto_update, bg="#2b2b2b", fg="white", selectcolor="#2b2b2b").pack(pady=5)
        Radiobutton(param_frame, text="U2NetP", variable=self.selected_model, value=2, command=self.check_auto_update, bg="#2b2b2b", fg="white", selectcolor="#2b2b2b").pack(pady=5)
        Radiobutton(param_frame, text="Silueta", variable=self.selected_model, value=3, command=self.check_auto_update, bg="#2b2b2b", fg="white", selectcolor="#2b2b2b").pack(pady=5)

        # Case à cocher : désactiver pour éviter les lenteurs
        Checkbutton(param_frame, text="Use alpha mapping", variable=self.use_alpha_matting, bg="#2b2b2b", fg="white", selectcolor="#2b2b2b").pack(pady=10)
        

        # Sliders pour les paramètres
        self.foreground_slider = SliderWithEntry(param_frame, "Foreground", 0, 255, default_value=240)
        self.background_slider = SliderWithEntry(param_frame, "Background", 0, 255, default_value=10)
        self.erode_slider = SliderWithEntry(param_frame, "Erode Size", 0, 50, default_value=10)

        # Boutons principaux
        Button(param_frame, text="Update", command=self.update_preview, bg="#444", fg="white").pack(pady=10, fill="x")
        Button(param_frame, text="Save As", command=self.select_output_file, bg="#444", fg="white").pack(pady=10, fill="x")
        Button(param_frame, text="Do Whole Folder", command=lambda: self.process_whole_folder(do_all_models=False), bg="#444", fg="white").pack(pady=10, fill="x")
        Button(param_frame, text="Do Whole Folder with all models", command=lambda: self.process_whole_folder(do_all_models=True), bg="#444", fg="white").pack(pady=10, fill="x")
        
        # Label d'état (initialisé à "Ready")
        self.status_label = Label(param_frame, text="Select Input File", bg="#2b2b2b", fg="yellow", font=("Arial", 12))
        self.status_label.pack(side="bottom", fill="x", pady=5)



    def reload_app(self):
        """Quitte et relance l'application."""
        print("Redémarrage de l'application...")
        python = sys.executable  # Chemin de l'exécutable Python en cours
        os.execv(python, [python] + sys.argv)  # Relance le script avec les mêmes arguments

    def toggle_preview(self):
        """Gère l'affichage de l'aperçu original ou traité."""
        if self.show_original.get():
            self.display_preview(self.input_canvas, self.input_image)
        else:
            self.display_preview(self.input_canvas, self.output_image)

    def check_auto_update(self, *_):
        """Décocher 'Show Original' et réafficher la preview processed."""
        self.show_original.set(False)
        if self.auto_update.get():
            self.update_preview()

    def update_preview(self):
        self.process_image()

    def select_input_file(self):
        """Ouvre une boîte de dialogue pour sélectionner un fichier d'entrée."""
        self.input_file = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.input_file:
            self.input_image = Image.open(self.input_file)
            self.display_preview(self.input_canvas, self.input_image)
        self.process_image()
        self.update_status(f"Ready", "yellow")

    def display_preview(self, canvas, img):
        """Affiche une image dans un canvas avec fond en damier et ajustement aux proportions."""
        if not img:
            return
        img = img.convert("RGBA")

        # Taille du canvas
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        # Calcul de la nouvelle taille tout en respectant les proportions
        img_width, img_height = img.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        # Créer un damier pour simuler le fond transparent
        checkerboard = Image.new("RGBA", (new_width, new_height))
        draw = ImageDraw.Draw(checkerboard)
        square_size = 10
        for y in range(0, new_height, square_size):
            for x in range(0, new_width, square_size):
                color = (34, 139, 34, 255) if (x // square_size + y // square_size) % 2 == 0 else (46, 184, 46, 255)
                draw.rectangle([x, y, x + square_size, y + square_size], fill=color)

        # Superposer l'image redimensionnée
        preview = img.resize((new_width, new_height), Image.ANTIALIAS)
        preview = Image.alpha_composite(checkerboard, preview)

        # Afficher dans le canvas
        img_tk = ImageTk.PhotoImage(preview)
        canvas.img_tk = img_tk
        canvas.create_image((canvas_width - new_width) // 2, (canvas_height - new_height) // 2, anchor="nw", image=img_tk)

    def process_image(self):
        """Traite l'image en fonction des paramètres sélectionnés."""
        if not self.input_file:
            return
        
        self.update_status(f"Processing", "red")

        self.output_image = self.processor.process_image(
            self.input_image,
            self.selected_model.get(),
            self.use_alpha_matting.get(),
            self.foreground_slider.get(),
            self.background_slider.get(),
            self.erode_slider.get(),
            self.use_gpu.get()
        )
        self.display_preview(self.input_canvas, self.output_image)
        self.update_status(f"Done", "yellow")

    def on_resize(self, event):
        """Callback pour gérer le redimensionnement de la fenêtre."""
        canvas_width = self.input_canvas.winfo_width()
        canvas_height = self.input_canvas.winfo_height()
        print(f"Redimensionnement : largeur={canvas_width}, hauteur={canvas_height}")
        # Recalculer et redessiner la preview
        if self.input_image:
            self.display_preview(self.input_canvas, self.input_image if self.show_original.get() else self.output_image)


    def run(self):
        self.root.mainloop()

    def process_whole_folder(self, do_all_models=False):
        """Traite tous les fichiers image dans le même dossier que le fichier d'entrée."""
        if not self.input_file:
            print("Aucun fichier d'entrée sélectionné.")
            return

        # Récupérer le dossier d'entrée à partir du fichier d'entrée
        input_dir = os.path.dirname(self.input_file)

        # Demander à l'utilisateur de sélectionner un dossier de sortie
        self.output_dir = self.select_folder(self.output_dir if os.path.exists(self.output_dir) else self.root_dir, "Select output folder")
        if not os.path.exists(self.output_dir):
            print("Dossier de sortie introuvable.")
            return

        # Modèles disponibles
        models = {
            1: "u2net",
            2: "u2netp",
            3: "silueta"
        }
        
        self.update_status(f"Processing", "red")
        old_INP = self.inp
        # Itérer sur tous les fichiers image dans le dossier d'entrée
        for file_name in os.listdir(input_dir):
            input_path = os.path.join(input_dir, file_name)

            # Vérifier si le fichier est une image
            if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                try:
                    # Charger l'image d'entrée
                    inp = Image.open(input_path)

                    # Traiter l'image avec un ou plusieurs modèles
                    if do_all_models:
                        for model_id, model_name in models.items():
                            output = self.processor.process_image(
                                inp,
                                model_id,  # Utiliser chaque modèle successivement
                                self.use_alpha_matting.get(),
                                self.foreground_slider.get(),
                                self.background_slider.get(),
                                self.erode_slider.get(),
                                self.use_gpu.get()
                            )

                            # Générer un chemin de sortie unique pour chaque modèle
                            base_name = os.path.splitext(file_name)[0]
                            output_path = os.path.join(self.output_dir, f"{base_name}_no_bg_{model_name}.png")
                            count = 0
                            while os.path.exists(output_path):
                                count += 1
                                output_path = os.path.join(self.output_dir, f"{base_name}_no_bg_{model_name}_{count:03d}.png")

                            # Sauvegarder l'image sortie
                            output.save(output_path)
                            print(f"Image sauvegardée : {output_path}")
                    else:
                        # Traiter avec le modèle sélectionné uniquement
                        output = self.processor.process_image(
                            inp,
                            self.selected_model.get(),
                            self.use_alpha_matting.get(),
                            self.foreground_slider.get(),
                            self.background_slider.get(),
                            self.erode_slider.get(),
                            self.use_gpu.get()
                        )

                        # Générer un chemin de sortie unique
                        base_name = os.path.splitext(file_name)[0]
                        output_path = os.path.join(self.output_dir, f"{base_name}_no_bg.png")
                        count = 0
                        while os.path.exists(output_path):
                            count += 1
                            output_path = os.path.join(self.output_dir, f"{base_name}_no_bg_{count:03d}.png")

                        # Sauvegarder l'image sortie
                        output.save(output_path)
                        print(f"Image sauvegardée : {output_path}")

                except Exception as e:
                    print(f"Erreur lors du traitement de {file_name}: {e}")

        self.update_status(f"All files done", "yellow")


    def select_folder(self, init_dir, title):
        dir = filedialog.askdirectory(initialdir=init_dir, title=title)

        # Vérifier si le chemin sélectionné existe
        if not os.path.exists(dir):
            # Si le chemin complet n'existe pas, tester le parent
            parent_dir = os.path.dirname(dir)
            if os.path.exists(dir):
                dir = parent_dir
            else:
                print("Le chemin sélectionné est invalide.")
                return
        return dir

    def select_output_file(self):
        """Ouvre une boîte de dialogue pour enregistrer la preview de l'image traitée."""
        if not self.output_image:
            print("Aucune image à enregistrer. Veuillez traiter une image d'abord.")
            return

        # Ouvrir une boîte de dialogue pour sélectionner le chemin de sauvegarde
        self.output_file = filedialog.asksaveasfilename(
            initialdir=self.output_dir,
            initialfile=os.path.splitext(os.path.basename(self.input_file))[0] + "_no_bg.png",
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png")]
        )

        # Vérifier si un fichier a été sélectionné
        if not self.output_file:
            print("Aucun fichier de sortie sélectionné.")
            return

        # Sauvegarder l'image traitée
        try:
            self.output_image.save(self.output_file)
            self.update_status(f"Done : {self.output_file}", "yellow")
        except Exception as e:
            print(f"Erreur lors de l'enregistrement de l'image : {e}")

    def update_status(self, message, color):
        """
        Met à jour le label d'état avec un message et une couleur spécifiques.

        :param message: Texte à afficher dans le label d'état.
        :param color: Couleur du texte (par exemple, "red", "yellow", "green").
        """
        self.status_label.config(text=message, fg=color)
        self.root.update_idletasks()  # Met à jour immédiatement l'interface
        print (message)

