import customtkinter as ctk
import math

class PoliceScannerPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Variable pour l'animation de l'onde
        self.phase = 0
        self.is_active = False

        # --- TITRE DE LA PAGE ---
        self.title_label = ctk.CTkLabel(
            self, 
            text="📻 Scanner Radio Police", 
            font=ctk.CTkFont(family="Courier", size=24, weight="bold"),
            text_color="#66fcf1"
        )
        self.title_label.pack(pady=(20, 10))

        # --- ÉCRAN DE L'ONDE (CANVAS) ---
        # Un espace noir cyber pour dessiner l'onde en temps réel
        self.canvas = ctk.CTkCanvas(
            self, 
            width=500, 
            height=120, 
            bg="#131820", 
            highlightthickness=1, 
            highlightbackground="#45a29e"
        )
        self.canvas.pack(pady=15, padx=20)
        
        # Dessiner l'onde plate initiale au démarrage
        self.draw_flat_wave()

        # --- AFFICHAGE DE LA FRÉQUENCE (XX.yy) ---
        self.freq_label = ctk.CTkLabel(
            self, 
            text="00.00 MHz", 
            font=ctk.CTkFont(family="Courier", size=32, weight="bold"),
            text_color="#66fcf1"
        )
        self.freq_label.pack(pady=10)

        # --- RÉGLETTES DE SÉLECTION ---
        # Réglette XX (00 à 99)
        self.label_x = ctk.CTkLabel(self, text="Fréquence Principale (XX) :", font=ctk.CTkFont(family="Courier", size=14), text_color="#c5c6c7")
        self.label_x.pack(pady=(10, 2))
        
        self.slider_x = ctk.CTkSlider(
            self, from_=0, to=99, number_of_steps=99, 
            command=self.update_frequency,
            button_color="#45a29e", button_hover_color="#66fcf1", progress_color="#45a29e"
        )
        self.slider_x.set(0)
        self.slider_x.pack(pady=5, padx=40, fill="x")

        # Réglette yy (00 à 99)
        self.label_y = ctk.CTkLabel(self, text="Sous-Fréquence (yy) :", font=ctk.CTkFont(family="Courier", size=14), text_color="#c5c6c7")
        self.label_y.pack(pady=(15, 2))
        
        self.slider_y = ctk.CTkSlider(
            self, from_=0, to=99, number_of_steps=99, 
            command=self.update_frequency,
            button_color="#45a29e", button_hover_color="#66fcf1", progress_color="#45a29e"
        )
        self.slider_y.set(0)
        self.slider_y.pack(pady=5, padx=40, fill="x")

        # --- TOGGLE D'ACTIVATION (SWITCH) ---
        self.radio_switch = ctk.CTkSwitch(
            self, 
            text="Intercepter la fréquence", 
            command=self.toggle_radio, 
            font=ctk.CTkFont(family="Courier", size=16, weight="bold"),
            text_color="#66fcf1",
            progress_color="#00CC66"
        )
        self.radio_switch.pack(pady=25)

    def update_frequency(self, _=None):
        """Met à jour le texte XX.yy avec toujours deux chiffres visibles."""
        val_x = int(self.slider_x.get())
        val_y = int(self.slider_y.get())
        # Le format :02d force l'affichage de deux chiffres (ex: 05 au lieu de 5)
        self.freq_label.configure(text=f"{val_x:02d}.{val_y:02d} MHz")

    def draw_flat_wave(self):
        """Dessine une ligne plate parfaite au milieu du canvas."""
        self.canvas.delete("all")
        # Ligne horizontale centrée (Y = 60 sur un canvas de hauteur 120)
        self.canvas.create_line(0, 60, 500, 60, fill="#45a29e", width=2, tags="wave")

    def animate_wave(self):
        """Génère une onde sinusoïdale qui bouge selon la fréquence choisie."""
        if not self.is_active:
            return

        self.canvas.delete("all")
        
        val_x = int(self.slider_x.get())
        val_y = int(self.slider_y.get())

        # Calculs pour changer la forme de l'onde selon XX et yy
        frequency_modifier = 0.05 + (val_x / 500.0)  # XX change la répétition des vagues
        amplitude = 10 + (val_y / 3.0)               # yy change la hauteur des vagues

        points = []
        # On calcule les coordonnées Y pour chaque pixel X du canvas
        for x in range(0, 505, 5):
            # Formule mathématique de l'onde avec la phase qui avance pour faire l'effet de mouvement
            y = 60 + amplitude * math.sin((x * frequency_modifier) + self.phase)
            points.append((x, y))

        # Dessin de l'onde dynamique sur le canvas
        for i in range(len(points) - 1):
            self.canvas.create_line(
                points[i][0], points[i][1], 
                points[i+1][0], points[i+1][1], 
                fill="#66fcf1", width=2, tags="wave"
            )

        # Avancement de la phase pour le prochain rafraîchissement
        self.phase += 0.2
        
        # Relance la fonction toutes les 30 millisecondes pour une animation fluide
        self.after(30, self.animate_wave)

    def toggle_radio(self):
        """Active ou désactive la radio et met à jour les logs système."""
        val_x = int(self.slider_x.get())
        val_y = int(self.slider_y.get())

        if self.radio_switch.get() == 1:
            self.is_active = True
            self.animate_wave()
            if hasattr(self.master, 'add_log'):
                self.master.add_log(f"RADIO : Connexion établie sur le canal {val_x:02d}.{val_y:02d} MHz.")
        else:
            self.is_active = False
            self.draw_flat_wave()
            if hasattr(self.master, 'add_log'):
                self.master.add_log("RADIO : Déconnexion du flux audio. Signal perdu.")