# modules/ui/pc_cloner.py
import customtkinter as ctk
import random
import threading
import time

class PCClonerPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.is_cloning = False
        self.clone_progress = 0
        self.clone_finished = False
        self.current_drives = []
        self.total_files = 0
        self.files_done = 0
        self.hack_duration = 0
        self.start_time = 0

        self.DRIVE_BRANDS = [
            "Kingston DataTraveler", "Samsung Bar Plus", "SanDisk Ultra",
            "WD My Passport", "Seagate Backup Plus", "Toshiba Canvio",
            "Corsair Flash Voyager", "PNY Turbo", "Lexar JumpDrive",
            "Crucial X8 SSD", "ADATA UV150", "Transcend JetFlash"
        ]

        self.FAKE_FILES_POOL = [
            "Documents/", "Pictures/", "Videos/", "Downloads/", "Desktop/",
            "AppData/", "Program Files/", "Windows/System32/", "Users/",
            ".ssh/keys/", "Crypto_Wallets/", "Passwords.txt", "Banking_Info/",
            "Contacts.vcf", "Emails_Backup/", "Tax_Documents/", "Photos_Perso/",
            "Project_Confidential/", "Browser_History.db", "Saved_Passwords.csv"
        ]

        # --- TITRE ---
        self.title_label = ctk.CTkLabel(
            self,
            text="💾 PC Cloner - USB Drive Detection",
            font=ctk.CTkFont(family="Courier", size=22, weight="bold"),
            text_color="#00ff00"
        )
        self.title_label.pack(pady=(15, 10))

        # --- DÉTECTION DE DISQUE ---
        self.detection_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", border_width=2, border_color="#00ff00")
        self.detection_frame.pack(pady=10, padx=15, fill="x")

        self.detection_label = ctk.CTkLabel(
            self.detection_frame,
            text="🔍 Disques détectés :",
            font=ctk.CTkFont(family="Courier", size=12, weight="bold"),
            text_color="#00ff00"
        )
        self.detection_label.pack(pady=(10, 5), padx=10, anchor="w")

        self.drive_listbox = ctk.CTkTextbox(
            self.detection_frame,
            height=60,
            font=ctk.CTkFont(family="Courier", size=9),
            text_color="#00ff00",
            fg_color="#0a0a0a",
            border_color="#00ff00",
            border_width=1
        )
        self.drive_listbox.pack(pady=5, padx=10, fill="x")
        self.drive_listbox.configure(state="disabled")

        self.scan_btn = ctk.CTkButton(
            self.detection_frame,
            text="🔄 Scanner",
            command=self.scan_drives,
            font=ctk.CTkFont(family="Courier", size=9, weight="bold"),
            fg_color="#ff0000",
            hover_color="#cc0000",
            height=28
        )
        self.scan_btn.pack(pady=8, padx=10, fill="x")

        # --- SÉLECTION DE DISQUE ---
        self.select_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.select_frame.pack(pady=8, padx=15, fill="x")

        self.select_label = ctk.CTkLabel(
            self.select_frame,
            text="Source :",
            font=ctk.CTkFont(family="Courier", size=10, weight="bold"),
            text_color="#ffb703"
        )
        self.select_label.pack(side="left", padx=5)

        self.selected_drive = ctk.StringVar(value="Aucun")
        self.drive_menu = ctk.CTkOptionMenu(
            self.select_frame,
            variable=self.selected_drive,
            values=["Aucun"],
            font=ctk.CTkFont(family="Courier", size=9),
            button_color="#45a29e",
            button_hover_color="#66fcf1",
        )
        self.drive_menu.pack(side="left", padx=5, fill="x", expand=True)

        # --- BARRE DE PROGRESSION ---
        self.progress_label = ctk.CTkLabel(
            self,
            text="Prêt à cloner",
            font=ctk.CTkFont(family="Courier", size=10, weight="bold"),
            text_color="#c5c6c7"
        )
        self.progress_label.pack(pady=(10, 3))

        self.progress_bar = ctk.CTkProgressBar(
            self,
            progress_color="#00ff00",
            fg_color="#1a1a1a",
            border_color="#00ff00",
            border_width=1
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=3, padx=15, fill="x")

        # Stats + timer
        self.stats_label = ctk.CTkLabel(
            self,
            text="Vitesse : 0 MB/s  |  Fichiers : 0/0  |  ⏱ 0s",
            font=ctk.CTkFont(family="Courier", size=9),
            text_color="#66fcf1"
        )
        self.stats_label.pack(pady=3)

        # --- BOUTONS D'ACTION (EN DESSOUS DE LA BARRE) ---
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(pady=8, padx=15, fill="x")

        self.clone_btn = ctk.CTkButton(
            self.action_frame,
            text="▶ CLONER",
            command=self.start_clone,
            font=ctk.CTkFont(family="Courier", size=10, weight="bold"),
            fg_color="#00ff00",
            hover_color="#00cc00",
            text_color="#000000",
            height=32
        )
        self.clone_btn.pack(side="left", padx=3, fill="both", expand=True)

        self.stop_btn = ctk.CTkButton(
            self.action_frame,
            text="⏹ STOP",
            command=self.stop_clone,
            font=ctk.CTkFont(family="Courier", size=10, weight="bold"),
            fg_color="#ff0000",
            hover_color="#cc0000",
            height=32,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=3, fill="both", expand=True)

        # --- BOUTON DE CONFIRMATION (JUSTE SOUS LES BOUTONS) ---
        self.confirm_btn = ctk.CTkButton(
            self,
            text="✅ CONFIRMER LE TRANSFERT",
            command=self.confirm_transfer,
            font=ctk.CTkFont(family="Courier", size=11, weight="bold"),
            fg_color="#00cc00",
            hover_color="#009900",
            text_color="#000000",
            height=36,
            state="disabled"
        )
        self.confirm_btn.pack(pady=8, padx=15, fill="x")

        # --- FICHIERS ---
        self.files_label = ctk.CTkLabel(
            self,
            text="📂 Fichiers détectés :",
            font=ctk.CTkFont(family="Courier", size=10, weight="bold"),
            text_color="#ffb703"
        )
        self.files_label.pack(pady=(8, 3), padx=15, anchor="w")

        self.files_listbox = ctk.CTkTextbox(
            self,
            height=80,
            font=ctk.CTkFont(family="Courier", size=8),
            text_color="#00ff00",
            fg_color="#0a0a0a",
            border_color="#00ff00",
            border_width=1
        )
        self.files_listbox.pack(pady=3, padx=15, fill="both", expand=True)
        self.files_listbox.configure(state="disabled")

    def generate_random_drives(self, count=3):
        """Génère `count` disques aléatoires avec noms et tailles réalistes."""
        chosen_brands = random.sample(self.DRIVE_BRANDS, count)
        possible_sizes = [16, 32, 64, 128, 256, 512, 1024, 2048]
        drives = []
        for brand in chosen_brands:
            size = random.choice(possible_sizes)
            drives.append({"name": brand, "size": size})
        return drives

    def scan_drives(self):
        """Scanne et génère des disques aléatoires."""
        self.drive_listbox.configure(state="normal")
        self.drive_listbox.delete("1.0", "end")

        self.current_drives = self.generate_random_drives(3)

        text = "[SCAN] Recherche des USB...\n"
        for drive in self.current_drives:
            text += f"✓ {drive['name']} ({drive['size']}GB)\n"

        self.drive_listbox.insert("1.0", text)
        self.drive_listbox.configure(state="disabled")

        # Met à jour le menu déroulant avec les nouveaux disques
        drive_names = [d["name"] for d in self.current_drives]
        self.drive_menu.configure(values=drive_names)
        self.selected_drive.set(drive_names[0])

    def start_clone(self):
        """Lance le clonage du disque sélectionné."""
        if not self.current_drives or self.selected_drive.get() == "Aucun":
            self.progress_label.configure(text="⚠ Scannez d'abord un disque !")
            return

        # Reset état
        self.is_cloning = True
        self.clone_finished = False
        self.clone_progress = 0
        self.files_done = 0

        # Génère un nombre de fichiers aléatoire et une durée aléatoire
        self.total_files = random.randint(50, 500)
        self.hack_duration = random.uniform(6, 18)  # secondes
        self.start_time = time.time()

        self.confirm_btn.configure(state="disabled")

        self.clone_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.drive_menu.configure(state="disabled")
        self.scan_btn.configure(state="disabled")

        thread = threading.Thread(target=self.perform_clone)
        thread.daemon = True
        thread.start()

    def perform_clone(self):
        """Effectue le clonage avec barre de progression et timer."""
        selected_files = random.sample(
            self.FAKE_FILES_POOL, min(len(self.FAKE_FILES_POOL), 10)
        )

        # Affiche les fichiers détectés
        self.files_listbox.configure(state="normal")
        self.files_listbox.delete("1.0", "end")
        files_text = ""
        for f in selected_files:
            files_text += f"🔍 {f}\n"
        self.files_listbox.insert("1.0", files_text)
        self.files_listbox.configure(state="disabled")

        while self.is_cloning and self.clone_progress < 100:
            elapsed = time.time() - self.start_time
            self.clone_progress = min(100, (elapsed / self.hack_duration) * 100)

            self.files_done = int((self.clone_progress / 100) * self.total_files)
            speed = random.uniform(20, 250)

            self.progress_bar.set(self.clone_progress / 100)
            self.progress_label.configure(text=f"Clonage... {self.clone_progress:.1f}%")
            self.stats_label.configure(
                text=f"Vitesse : {speed:.1f} MB/s  |  Fichiers : {self.files_done}/{self.total_files}  |  ⏱ {elapsed:.1f}s"
            )

            time.sleep(0.2)

        if self.is_cloning:
            self.clone_progress = 100
            self.files_done = self.total_files
            self.progress_bar.set(1.0)
            self.progress_label.configure(text="✓ Clonage terminé ! En attente de confirmation...")
            elapsed = time.time() - self.start_time
            self.stats_label.configure(
                text=f"Vitesse : 0 MB/s  |  Fichiers : {self.files_done}/{self.total_files}  |  ⏱ {elapsed:.1f}s"
            )
            self.clone_finished = True
            self.confirm_btn.configure(state="normal")

        self.is_cloning = False
        self.clone_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.drive_menu.configure(state="normal")
        self.scan_btn.configure(state="normal")

    def stop_clone(self):
        """Arrête le clonage."""
        self.is_cloning = False
        self.progress_label.configure(text="⏹ Clonage annulé")
        self.clone_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.drive_menu.configure(state="normal")
        self.scan_btn.configure(state="normal")
        self.confirm_btn.configure(state="disabled")

    def confirm_transfer(self):
        """Confirme le transfert final des données clonées."""
        self.progress_label.configure(text="✅ Transfert confirmé et terminé !")
        self.confirm_btn.configure(state="disabled", text="✅ TRANSFERT EFFECTUÉ")

        if hasattr(self.master, 'add_log'):
            drive = self.selected_drive.get()
            self.master.add_log(f"💾 PC CLONER : Transfert confirmé depuis {drive} ({self.files_done} fichiers)")