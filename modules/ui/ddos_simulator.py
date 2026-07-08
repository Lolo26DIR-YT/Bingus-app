# ddos_simulator.py
import customtkinter as ctk
import random

class DDosSimulatorPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.is_attacking = False
        self.attack_type = "SYN Flood"

        # Puissances d'attaque en Gbps
        self.POWER_LEVELS = [0.5, 1, 2, 5, 10, 25, 50, 100, 250, 500]
        self.ATTACK_TYPES = ["SYN Flood", "UDP Flood", "HTTP Flood", "DNS Amplification", "NTP Reflection"]

        # --- TITRE ---
        self.title_label = ctk.CTkLabel(
            self,
            text="🌊 Générateur DDoS",
            font=ctk.CTkFont(family="Courier", size=24, weight="bold"),
            text_color="#66fcf1"
        )
        self.title_label.pack(pady=(15, 5))

        # --- TYPE D'ATTAQUE ---
        self.attack_type_label = ctk.CTkLabel(
            self,
            text="Type d'attaque : SYN Flood",
            font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
            text_color="#ffb703"
        )
        self.attack_type_label.pack(pady=(5, 10))

        # Boutons de sélection du type
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=5, padx=15, fill="x")
        
        for i, attack in enumerate(self.ATTACK_TYPES):
            btn = ctk.CTkButton(
                self.button_frame,
                text=attack,
                command=lambda a=attack: self.select_attack(a),
                font=ctk.CTkFont(family="Courier", size=9, weight="bold"),
                fg_color="#45a29e",
                hover_color="#66fcf1",
                height=25
            )
            btn.pack(side="left", padx=2, fill="x", expand=True)

        # --- PUISSANCE D'ATTAQUE ---
        self.power_label = ctk.CTkLabel(
            self,
            text="Puissance : 2 Gbps",
            font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
            text_color="#c5c6c7"
        )
        self.power_label.pack(pady=(15, 3))

        self.power_slider = ctk.CTkSlider(
            self,
            from_=0,
            to=len(self.POWER_LEVELS) - 1,
            number_of_steps=len(self.POWER_LEVELS) - 1,
            command=self.update_power,
            button_color="#FF4C4C",
            button_hover_color="#ff6b6b",
            progress_color="#FF4C4C"
        )
        self.power_slider.set(2)
        self.power_slider.pack(pady=5, padx=30, fill="x")

        # --- AFFICHAGE TEMPS RÉEL ---
        self.stats_frame = ctk.CTkFrame(self, fg_color="#131820", border_width=1, border_color="#45a29e")
        self.stats_frame.pack(pady=10, padx=15, fill="x")

        self.packets_label = ctk.CTkLabel(
            self.stats_frame,
            text="Paquets/sec : 0",
            font=ctk.CTkFont(family="Courier", size=11),
            text_color="#66fcf1"
        )
        self.packets_label.pack(pady=3)

        self.bandwidth_label = ctk.CTkLabel(
            self.stats_frame,
            text="Bande passante : 0 Gbps",
            font=ctk.CTkFont(family="Courier", size=11),
            text_color="#66fcf1"
        )
        self.bandwidth_label.pack(pady=3)

        self.targets_label = ctk.CTkLabel(
            self.stats_frame,
            text="Targets actives : 0",
            font=ctk.CTkFont(family="Courier", size=11),
            text_color="#66fcf1"
        )
        self.targets_label.pack(pady=3)

        # --- BOUTONS DE CONTRÔLE ---
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.pack(pady=10, padx=15, fill="x")

        self.start_button = ctk.CTkButton(
            self.control_frame,
            text="▶ LANCER",
            command=lambda: self.toggle_attack(True),
            font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
            fg_color="#FF4C4C",
            hover_color="#ff6b6b",
            text_color="white",
            height=35,
            corner_radius=6
        )
        self.start_button.pack(side="left", padx=3, fill="x", expand=True)

        self.stop_button = ctk.CTkButton(
            self.control_frame,
            text="⏹ ARRÊTER",
            command=lambda: self.toggle_attack(False),
            font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
            fg_color="#45a29e",
            hover_color="#66fcf1",
            text_color="white",
            height=35,
            corner_radius=6
        )
        self.stop_button.pack(side="left", padx=3, fill="x", expand=True)

    def select_attack(self, attack_type):
        """Change le type d'attaque sélectionné."""
        self.attack_type = attack_type
        self.attack_type_label.configure(text=f"Type d'attaque : {attack_type}")

    def update_power(self, value):
        """Met à jour la puissance d'attaque."""
        index = int(round(float(value)))
        power = self.POWER_LEVELS[index]
        self.power_label.configure(text=f"Puissance : {power} Gbps")

    def update_stats(self):
        """Mise à jour en temps réel des stats (quand l'attaque est active)."""
        if not self.is_attacking:
            return

        index = int(round(self.power_slider.get()))
        power = self.POWER_LEVELS[index]

        # Calcul fictif des paquets
        pps = int(power * 1000000 + random.randint(-50000, 50000))
        bandwidth = power + random.uniform(-0.5, 0.5)
        targets = random.randint(50, 500)

        self.packets_label.configure(text=f"Paquets/sec : {pps:,}")
        self.bandwidth_label.configure(text=f"Bande passante : {bandwidth:.2f} Gbps")
        self.targets_label.configure(text=f"Targets actives : {targets}")

        self.after(1500, self.update_stats)

    def toggle_attack(self, state):
        """Active/Désactive l'attaque DDoS."""
        index = int(round(self.power_slider.get()))
        power = self.POWER_LEVELS[index]

        if state:
            self.is_attacking = True
            self.power_slider.configure(state="disabled")

            self.packets_label.configure(text="Paquets/sec : Calcul...", text_color="#00CC66")
            self.bandwidth_label.configure(text="Bande passante : Calcul...", text_color="#00CC66")
            self.targets_label.configure(text="Targets actives : Calcul...", text_color="#00CC66")

            self.update_stats()

            if hasattr(self.master, 'add_log'):
                self.master.add_log(f"🌊 DDOS : Attaque lancée ({self.attack_type}) - Puissance : {power} Gbps")
        else:
            self.is_attacking = False
            self.power_slider.configure(state="normal")

            self.packets_label.configure(text="Paquets/sec : 0", text_color="#66fcf1")
            self.bandwidth_label.configure(text="Bande passante : 0 Gbps", text_color="#66fcf1")
            self.targets_label.configure(text="Targets actives : 0", text_color="#66fcf1")

            if hasattr(self.master, 'add_log'):
                self.master.add_log("🌊 DDOS : Attaque stoppée. Canaux fermés.")