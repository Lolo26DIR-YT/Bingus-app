# network_sniffer.py
import customtkinter as ctk
import random

class NetworkSnifferPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.is_sniffing = False
        self.packet_count = 0

        # Protocoles à afficher
        self.PROTOCOLS = ["HTTP", "HTTPS", "DNS", "FTP", "SMTP", "SSH", "TCP", "UDP", "ICMP"]
        
        # Ports courants
        self.COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3389, 8080, 8443]
        
        # Niveaux de filtrage
        self.FILTERS = ["Tous les paquets", "HTTP/HTTPS", "DNS", "SSH/FTP", "P2P/Torrents"]

        # --- TITRE ---
        self.title_label = ctk.CTkLabel(
            self,
            text="🔍 Analyseur Réseau (Sniffer)",
            font=ctk.CTkFont(family="Courier", size=24, weight="bold"),
            text_color="#66fcf1"
        )
        self.title_label.pack(pady=(15, 5))

        # --- STATS EN TEMPS RÉEL ---
        self.stats_frame = ctk.CTkFrame(self, fg_color="#131820", border_width=1, border_color="#45a29e")
        self.stats_frame.pack(pady=10, padx=15, fill="x")

        self.packet_count_label = ctk.CTkLabel(
            self.stats_frame,
            text="Paquets capturés : 0",
            font=ctk.CTkFont(family="Courier", size=11, weight="bold"),
            text_color="#66fcf1"
        )
        self.packet_count_label.pack(pady=3)

        self.data_volume_label = ctk.CTkLabel(
            self.stats_frame,
            text="Volume capturé : 0 MB",
            font=ctk.CTkFont(family="Courier", size=11, weight="bold"),
            text_color="#66fcf1"
        )
        self.data_volume_label.pack(pady=3)

        self.protocol_label = ctk.CTkLabel(
            self.stats_frame,
            text="Protocole détecté : Aucun",
            font=ctk.CTkFont(family="Courier", size=11, weight="bold"),
            text_color="#ffb703"
        )
        self.protocol_label.pack(pady=3)

        # --- AFFICHAGE DES PAQUETS ---
        self.packet_display = ctk.CTkTextbox(
            self,
            height=120,
            font=ctk.CTkFont(family="Courier", size=9),
            fg_color="#131820",
            border_width=1,
            border_color="#45a29e",
            text_color="#00CC66"
        )
        self.packet_display.pack(pady=8, padx=15, fill="both", expand=True)
        self.packet_display.insert("0.0", "[SYSTEM] Renifleur en attente d'activation...\n")
        self.packet_display.configure(state="disabled")

        # --- SÉLECTION DU FILTRE ---
        self.filter_label = ctk.CTkLabel(
            self,
            text="Filtre de capture : Tous les paquets",
            font=ctk.CTkFont(family="Courier", size=11, weight="bold"),
            text_color="#c5c6c7"
        )
        self.filter_label.pack(pady=(8, 3))

        self.filter_optionmenu = ctk.CTkOptionMenu(
            self,
            values=self.FILTERS,
            command=self.set_filter,
            button_color="#45a29e",
            button_hover_color="#66fcf1",
            fg_color="#131820",
            text_color="#66fcf1",
            font=ctk.CTkFont(family="Courier", size=10)
        )
        self.filter_optionmenu.set("Tous les paquets")
        self.filter_optionmenu.pack(pady=5, padx=30, fill="x")

        # --- BOUTONS DE CONTRÔLE ---
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.pack(pady=10, padx=15, fill="x")

        self.start_button = ctk.CTkButton(
            self.control_frame,
            text="▶ DÉMARRER",
            command=lambda: self.toggle_sniffer(True),
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
            text="⏹ ARRÊTER",
            command=lambda: self.toggle_sniffer(False),
            font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
            fg_color="#45a29e",
            hover_color="#66fcf1",
            text_color="white",
            height=35,
            corner_radius=6
        )
        self.stop_button.pack(side="left", padx=3, fill="x", expand=True)

        self.current_filter = "Tous les paquets"

    def set_filter(self, filter_name):
        """Change le filtre de capture."""
        self.current_filter = filter_name
        self.filter_label.configure(text=f"Filtre de capture : {filter_name}")

    def generate_fake_packet(self):
        """Génère une ligne de paquet fictive."""
        protocol = random.choice(self.PROTOCOLS)
        src_ip = f"{random.randint(192,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        dst_ip = f"{random.randint(10,172)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        port = random.choice(self.COMMON_PORTS)
        size = random.randint(64, 1500)
        
        return f"[{protocol:6}] {src_ip}:{port} → {dst_ip}:{port} | {size} bytes"

    def run_sniffing(self):
        """Boucle de capture de paquets."""
        if not self.is_sniffing:
            return

        # Génère 3-7 paquets par cycle
        for _ in range(random.randint(3, 7)):
            self.packet_count += 1
            packet_line = self.generate_fake_packet()

            self.packet_display.configure(state="normal")
            self.packet_display.insert("1.0", packet_line + "\n")
            self.packet_display.configure(state="disabled")

        # Mise à jour des stats
        protocol = random.choice(self.PROTOCOLS)
        volume = round(self.packet_count * 0.5, 2)

        self.packet_count_label.configure(text=f"Paquets capturés : {self.packet_count}")
        self.data_volume_label.configure(text=f"Volume capturé : {volume} MB")
        self.protocol_label.configure(text=f"Protocole détecté : {protocol}")

        self.after(1200, self.run_sniffing)

    def toggle_sniffer(self, state):
        """Active/Désactive le renifleur."""
        if state:
            self.is_sniffing = True
            self.packet_count = 0
            self.filter_optionmenu.configure(state="disabled")

            self.packet_display.configure(state="normal")
            self.packet_display.delete("1.0", "end")
            self.packet_display.insert("0.0", f"[INIT] Capture lancée - Filtre : {self.current_filter}\n")
            self.packet_display.insert("1.0", "—" * 70 + "\n")
            self.packet_display.configure(state="disabled")

            self.run_sniffing()

            if hasattr(self.master, 'add_log'):
                self.master.add_log(f"🔍 SNIFFER : Capture réseau démarrée ({self.current_filter})")
        else:
            self.is_sniffing = False
            self.filter_optionmenu.configure(state="normal")

            self.packet_display.configure(state="normal")
            self.packet_display.insert("1.0", f"[STOP] Capture terminée. {self.packet_count} paquets enregistrés.\n")
            self.packet_display.configure(state="disabled")

            if hasattr(self.master, 'add_log'):
                self.master.add_log(f"🔍 SNIFFER : Capture stoppée ({self.packet_count} paquets)")