import tkinter as tk

class SliderWithEntry:
    def __init__(self, parent, label, min_value, max_value, default_value=0, step=1):
        """
        Initialise un widget combiné Slider + Entry avec un titre, un slider, et un Entry.

        :param parent: Widget parent (Frame, Tk, etc.).
        :param label: Texte du label affiché à gauche de l'Entry.
        :param min_value: Valeur minimale du slider.
        :param max_value: Valeur maximale du slider.
        :param default_value: Valeur initiale du slider.
        :param step: Pas d'incrémentation du slider.
        """
        self.min_value = min_value
        self.max_value = max_value
        self.value = tk.IntVar(value=default_value)  # Variable Tkinter pour synchroniser slider et entry

        # Frame pour aligner le titre et l'Entry sur une seule ligne
        top_frame = tk.Frame(parent, bg="#2b2b2b")
        top_frame.pack(fill="x", pady=2)

        # Label pour le titre
        self.title_label = tk.Label(top_frame, text=label, bg="#2b2b2b", fg="white")
        self.title_label.pack(side="left", padx=5)

        # Champ Entry en dark mode
        self.entry = tk.Entry(
            top_frame,
            width=6,
            justify="center",
            bg="#444",  # Fond sombre
            fg="white",  # Texte clair
            insertbackground="white"  # Curseur blanc
        )
        self.entry.pack(side="right", padx=5)
        self.entry.insert(0, str(default_value))

        # Slider
        self.slider = tk.Scale(
            parent,
            from_=min_value,
            to=max_value,
            orient="horizontal",
            variable=self.value,
            resolution=step,
            command=self.update_entry,
            bg="#2b2b2b",
            fg="white",
            troughcolor="#444",
            highlightthickness=0,  # Supprime la bordure blanche
            showvalue=False  # Cache le chiffre par défaut
        )
        self.slider.pack(fill="x", pady=5)

        # Bindings
        self.entry.bind("<Return>", self.update_slider)  # Lorsqu'on appuie sur Entrée, mettre à jour le slider

    def update_entry(self, value):
        """Met à jour le champ Entry lorsque le slider change."""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(int(float(value))))

    def update_slider(self, event):
        """Met à jour le slider lorsque le champ Entry change."""
        try:
            # Limiter la valeur entre min_value et max_value
            value = int(self.entry.get())
            clamped_value = max(self.min_value, min(self.max_value, value))
            self.value.set(clamped_value)  # Met à jour la variable Tkinter synchronisée
            self.update_entry(clamped_value)  # Met à jour l'affichage dans l'Entry
        except ValueError:
            print("Entrée invalide, veuillez entrer un nombre.")

    def get(self):
        """Récupère la valeur actuelle."""
        return self.value.get()

    def set(self, value):
        """Définit une nouvelle valeur."""
        clamped_value = max(self.min_value, min(self.max_value, value))  # Clamp la valeur
        self.value.set(clamped_value)
        self.update_entry(clamped_value)
