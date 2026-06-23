import customtkinter as ctk

class IEMPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Liste des distances fixes imposées (en mètres)
        self.DISTANCES = [5, 10, 15, 20, 30, 50, 60, 70, 80, 90, 100, 150, 200]
        
        # Titre de la page
        self.title_label = ctk.CTkLabel(
            self, 
            text="⚡ Brouilleur IEM Portatif", 
            font=ctk.CTkFont(family="Courier", size=24, weight="bold"),
            text_color="#66fcf1"
        )
        self.title_label.pack(pady=(20, 10))

        # Statut Visuel (Rouge = Désactivé, Vert = Activé)
        self.status_label = ctk.CTkLabel(
            self, 
            text="Statut : DÉSACTIVÉ", 
            font=ctk.CTkFont(family="Courier", size=18, weight="bold"), 
            text_color="#FF4C4C"
        )
        self.status_label.pack(pady=10)

        # ---- SECTION RÉGLETTE (DISTANCE) ----
        self.distance_label = ctk.CTkLabel(
            self, 
            text="Rayon de brouillage : 15 m", 
            font=ctk.CTkFont(family="Courier", size=14),
            text_color="#c5c6c7"
        )
        self.distance_label.pack(pady=(30, 5))

        # La réglette va de 0 à 12 (les index de notre liste de 13 valeurs)
        # On met "number_of_steps" pour forcer le curseur à se caler pile sur les crans
        self.distance_slider = ctk.CTkSlider(
            self, 
            from_=0, 
            to=len(self.DISTANCES) - 1, 
            number_of_steps=len(self.DISTANCES) - 1,
            command=self.update_distance,
            button_color="#45a29e",
            button_hover_color="#66fcf1",
            progress_color="#45a29e"
        )
        # Par défaut on se met sur l'index 2 (ce qui correspond à 15 m)
        self.distance_slider.set(2)
        self.distance_slider.pack(pady=10, padx=20, fill="x")

        # ---- SECTION TOGGLE (ON/OFF) ----
        self.iem_switch = ctk.CTkSwitch(
            self, 
            text="Alimentation IEM", 
            command=self.toggle_iem, 
            font=ctk.CTkFont(family="Courier", size=16, weight="bold"),
            text_color="#66fcf1",
            progress_color="#00CC66"
        )
        self.iem_switch.pack(pady=40)

    def update_distance(self, value):
        """Convertit l'index de la réglette en valeur réelle de distance."""
        index = int(round(float(value)))
        distance = self.DISTANCES[index]
        self.distance_label.configure(text=f"Rayon de brouillage : {distance} m")

    def toggle_iem(self):
        """Gère l'état On/Off et verrouille ou déverrouille le curseur."""
        index_actuel = int(round(self.distance_slider.get()))
        distance_actuelle = self.DISTANCES[index_actuel]

        if self.iem_switch.get() == 1:
            # ON : On passe en vert et on bloque le curseur
            self.status_label.configure(text="Statut : ACTIVÉ ⚡", text_color="#00CC66")
            self.distance_slider.configure(state="disabled")
            
            # Envoi automatique du log dans la console de ton application principale
            if hasattr(self.master, 'add_log'):
                self.master.add_log(f"IEM : Onde de choc enclenchée ! Portée : {distance_actuelle}m.")
        else:
            # OFF : On repasse en rouge et on libère le curseur
            self.status_label.configure(text="Statut : DÉSACTIVÉ", text_color="#FF4C4C")
            self.distance_slider.configure(state="normal")
            
            if hasattr(self.master, 'add_log'):
                self.master.add_log("IEM : Système désactivé. Libération de la fréquence.")