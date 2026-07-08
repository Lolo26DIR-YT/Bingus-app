# gps_spoofer.py
import customtkinter as ctk
import random

class GpsSpoofferPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.is_spoofing = False

        # Coordonnées GPS réalistes (lat, lon, ville)
        self.LOCATIONS = [
            (48.8566, 2.3522, "Paris, France"),
            (51.5074, -0.1278, "Londres, UK"),
            (40.7128, -74.0060, "New York, USA"),
            (35.6762, 139.6503, "Tokyo, Japon"),
            (33.9425, 18.4240, "Cape Town, Afrique du Sud"),
            (37.7749, -122.4194, "San Francisco, USA"),
            (-33.8688, 151.2093, "Sydney, Australie"),
        ]

        # Niveaux de précision (en mètres)
        self.ACCURACY_LEVELS = [1, 5, 10, 25, 50, 100, 500, 1000]

        # --- TITRE ---
        self.title_label = ctk.CTkLabel(
            self,
            text="🗺️ Usurpateur de Position GPS",
            font=ctk.CTkFont(family="Courier", size=24, weight="bold"),
            text_color="#66fcf1"
        )
        self.title_label.pack(pady=(15, 5))

        # --- LOCALISATION ACTUELLE ---
        self.location_label = ctk.CTkLabel(
            self,
            text="Position actuelle : Indéterminée",
            font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
            text_color="#ffb703"
        )
        self.location_label.pack(pady=(5, 10))

        # --- BOUTONS DE LOCATIONS ---
        self.location_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.location_button_frame.pack(pady=5, padx=15, fill="x")

        for i, (lat, lon, city) in enumerate(self.LOCATIONS):
            btn = ctk.CTkButton(
                self.location_button_frame,
                text=city.split(',')[0],
                command=lambda l=city, la=lat, lo=lon: self.set_location(l, la, lo),
                font=ctk.CTkFont(family="Courier", size=9, weight="bold"),
                fg_color="#45a29e",
                hover_color="#66fcf1",
                height=25
            )
            btn.pack(side="left", padx=2, fill="x", expand=True)

        # --- COORDONNÉES GPS ---
        self.coords_frame = ctk.CTkFrame(self, fg_color="#131820", border_width=1, border_color="#45a29e")
        self.coords_frame.pack(pady=10, padx=15, fill="x")

        self.lat_label = ctk.CTkLabel(
            self.coords_frame,
            text="Latitude : 0.0000",
            font=ctk.CTkFont(family="Courier", size=11),
            text_color="#66fcf1"
        )
        self.lat_label.pack(pady=3)

        self.lon_label = ctk.CTkLabel(
            self.coords_frame,
            text="Longitude : 0.0000",
            font=ctk.CTkFont(family="Courier", size=11),
            text_color="#66fcf1"
        )
        self.lon_label.pack(pady=3)

        # --- PRÉCISION ---
        self.accuracy_label = ctk.CTkLabel(
            self,
            text="Précision de spoofing : 10 m",
            font=ctk.CTkFont(family="Courier", size=11, weight="bold"),
            text_color="#c5c6c7"
        )
        self.accuracy_label.pack(pady=(10, 3))

        self.accuracy_slider = ctk.CTkSlider(
            self,
            from_=0,
            to=len(self.ACCURACY_LEVELS) - 1,
            number_of_steps=len(self.ACCURACY_LEVELS) - 1,
            command=self.update_accuracy,
            button_color="#45a29e",
            button_hover_color="#66fcf1",
            progress_color="#45a29e"
        )
        self.accuracy_slider.set(2)
        self.accuracy_slider.pack(pady=5, padx=30, fill="x")

        # --- AFFICHAGE SIGNAL ---
        self.signal_label = ctk.CTkLabel(
            self,
            text="Qualité signal : 0/5",
            font=ctk.CTkFont(family="Courier", size=11),
            text_color="#66fcf1"
        )
        self.signal_label.pack(pady=5)

        # --- BOUTONS DE CONTRÔLE ---
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.pack(pady=10, padx=15, fill="x")

        self.start_button = ctk.CTkButton(
            self.control_frame,
            text="▶ ACTIVER",
            command=lambda: self.toggle_spoof(True),
            font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
            fg_color="#00CC66",
            hover_color="#33ff99",
            text_color="white",
            height=35,
            corner_radius=6
        )
        self.start_button.pack(side="left", padx=3, fill="x", expand=True)

        self.stop_button = ctk.CTkButton(
            self.control_frame,
            text="⏹ DÉSACTIVER",
            command=lambda: self.toggle_spoof(False),
            font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
            fg_color="#45a29e",
            hover_color="#66fcf1",
            text_color="white",
            height=35,
            corner_radius=6
        )
        self.stop_button.pack(side="left", padx=3, fill="x", expand=True)

        self.current_location = "Indéterminée"
        self.current_lat = 0.0
        self.current_lon = 0.0

    def set_location(self, city, lat, lon):
        """Change la localisation cible."""
        self.current_location = city
        self.current_lat = lat
        self.current_lon = lon
        self.location_label.configure(text=f"Position actuelle : {city}")
        self.lat_label.configure(text=f"Latitude : {lat:.4f}")
        self.lon_label.configure(text=f"Longitude : {lon:.4f}")

    def update_accuracy(self, value):
        """Met à jour la précision de spoofing."""
        index = int(round(float(value)))
        accuracy = self.ACCURACY_LEVELS[index]
        self.accuracy_label.configure(text=f"Précision de spoofing : {accuracy} m")

    def update_signal_quality(self):
        """Met à jour la qualité du signal en temps réel."""
        if not self.is_spoofing:
            return

        signal = random.randint(3, 5)
        bars = "█" * signal + "░" * (5 - signal)
        self.signal_label.configure(text=f"Qualité signal : {bars} ({signal}/5)")

        self.after(1000, self.update_signal_quality)

    def toggle_spoof(self, state):
        """Active/Désactive le spoofing GPS."""
        index = int(round(self.accuracy_slider.get()))
        accuracy = self.ACCURACY_LEVELS[index]

        if state:
            if self.current_location == "Indéterminée":
                self.location_label.configure(text="⚠️ Sélectionnez une localisation!", text_color="#FF4C4C")
                return

            self.is_spoofing = True
            self.accuracy_slider.configure(state="disabled")

            self.signal_label.configure(text_color="#00CC66")
            self.update_signal_quality()

            if hasattr(self.master, 'add_log'):
                self.master.add_log(f"🗺️ GPS SPOOF : Position falsifiée à {self.current_location} (±{accuracy}m)")
        else:
            self.is_spoofing = False
            self.accuracy_slider.configure(state="normal")

            self.signal_label.configure(text="Qualité signal : 0/5", text_color="#66fcf1")

            if hasattr(self.master, 'add_log'):
                self.master.add_log("🗺️ GPS SPOOF : Spoofing désactivé. Position réelle restaurée.")