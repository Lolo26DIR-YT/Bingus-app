import customtkinter as ctk
import random

class IMSICatcherPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.is_scanning = False
        
        # Opérateurs et modèles à la sauce américaine
        self.OPERATORS = ["AT&T", "Verizon", "T-Mobile", "Cricket Wireless"]
        self.PHONE_MODELS = ["iPhone 15 Pro", "Galaxy S24 Ultra", "Google Pixel 8", "iPhone 14"]

        # --- TITRE DE LA PAGE ---
        self.title_label = ctk.CTkLabel(
            self, 
            text="📡 Intercepteur IMSI Catcher", 
            font=ctk.CTkFont(family="Courier", size=22, weight="bold"),
            text_color="#66fcf1"
        )
        self.title_label.pack(pady=(20, 10))

        # --- CONSOLE D'INTERCEPTION ---
        self.console_label = ctk.CTkLabel(self, text="Flux de données cellulaires interceptées :", font=ctk.CTkFont(family="Courier", size=14), text_color="#c5c6c7")
        self.console_label.pack(pady=(10, 2), anchor="w", padx=20)

        self.terminal = ctk.CTkTextbox(
            self, 
            height=150, 
            font=ctk.CTkFont(family="Courier", size=11),
            fg_color="#131820", 
            border_width=1, 
            border_color="#45a29e",
            text_color="#66fcf1"
        )
        self.terminal.pack(pady=5, padx=20, fill="x")
        self.terminal.insert("0.0", "[SYSTEM] Awaiting cellular signal activation...\n")
        self.terminal.configure(state="disabled")

        # --- SECTION RÉGLETTE & SPÉCIFICATIONS RP ---
        self.range_label = ctk.CTkLabel(
            self, 
            text="Rayon : 10 m", 
            font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
            text_color="#66fcf1"
        )
        self.range_label.pack(pady=(15, 2))

        self.desc_label = ctk.CTkLabel(
            self, 
            text="Matériel : Non défini", 
            font=ctk.CTkFont(family="Courier", size=11, weight="bold"),
            text_color="#ffb703"
        )
        self.desc_label.pack(pady=(0, 5))

        # Réglette de 10 à 2000 mètres (Pas de 10 en 10 -> 199 étapes)
        self.range_slider = ctk.CTkSlider(
            self, 
            from_=10, 
            to=2000, 
            number_of_steps=199,
            command=self.update_range,
            button_color="#45a29e",
            button_hover_color="#66fcf1",
            progress_color="#45a29e"
        )
        self.range_slider.set(10)
        self.range_slider.pack(pady=5, padx=40, fill="x")

        # --- TOGGLE D'ACTIVATION ---
        self.scan_switch = ctk.CTkSwitch(
            self, 
            text="Injecter la fausse antenne (Cellular Relay Attack)", 
            command=self.toggle_scanner, 
            font=ctk.CTkFont(family="Courier", size=13, weight="bold"),
            text_color="#66fcf1",
            progress_color="#00CC66"
        )
        self.scan_switch.pack(pady=20)

        # Initialiser le texte de la réglette au démarrage
        self.update_range(10)

    def update_range(self, value):
        """Met à jour le texte et adapte la description RP selon la distance choisie."""
        val = int(round(float(value)))
        self.range_label.configure(text=f"Rayon de l'antenne : {val} m")

        # Logique des paliers de ton cahier des charges
        if 10 <= val <= 50:
            desc = "IMSI Compacte (sac a dos requis)"
        elif 50 < val <= 250:
            desc = "IMSI moyens - petit voiture compact requis"
        elif 250 < val <= 500:
            desc = "IMSI grand - voiture standart avec susprension modifié a 2 cran customitation Vmenu requis"
        elif 500 < val <= 1000:
            desc = "IMSI para-militaire - fourgon requis avec susprension modifié a 2 cran customitation Vmenu requis"
        else: # de 1000 à 2000
            desc = "IMSI militaire - camion requis avec susprension modifié a 2 cran customitation Vmenu requis"
        
        self.desc_label.configure(text=f"Logistique : {desc}")

    def generate_fake_us_data(self):
        """Génère une ligne d'interception complète au format américain."""
        # MCC US = 310, MNC fictif ou réel (ex: 410 pour AT&T)
        mcc = "310"
        mnc = str(random.choice([410, 120, 260, 560]))
        subscriber = "".join(str(random.randint(0, 9)) for _ in range(9))
        imsi = f"{mcc}-{mnc}-{subscriber}"
        
        # Format numéro américain : +1 (XXX) XXX-XXXX
        area_code = random.randint(200, 999)
        prefix = random.randint(200, 999)
        line_num = random.randint(1000, 9999)
        phone_number = f"+1 ({area_code}) {prefix}-{line_num}"
        
        # Force du signal de 0 à 20 avec un chiffre après la virgule
        signal = round(random.uniform(0.0, 20.0), 1)
        
        op = random.choice(self.OPERATORS)
        model = random.choice(self.PHONE_MODELS)
        dist = random.randint(5, max(11, int(self.range_slider.get())))
        
        return f"[CAPTURED] {op} | {model} | Phone: {phone_number}\n ↳ IMSI: {imsi} | Dist: {dist}m | Signal: {signal:0.1f}/20.0\n"

    def loop_capture(self):
        """Boucle de capture des données cellulaires."""
        if not self.is_scanning:
            return

        self.terminal.configure(state="normal")
        self.terminal.insert("1.0", self.generate_fake_us_data() + "—" * 55 + "\n")
        self.terminal.configure(state="disabled")

        # Intervalle aléatoire pour faire réaliste
        self.after(random.randint(1200, 3500), self.loop_capture)

    def toggle_scanner(self):
        """Bascule l'état On/Off et verrouille/déverrouille la réglette."""
        val = int(round(self.range_slider.get()))

        if self.scan_switch.get() == 1:
            self.is_scanning = True
            self.range_slider.configure(state="disabled")
            
            self.terminal.configure(state="normal")
            self.terminal.insert("1.0", f"[INFO] Tower spoofing initiated. Range set to {val}m...\n")
            self.terminal.configure(state="disabled")
            
            self.loop_capture()
            
            if hasattr(self.master, 'add_log'):
                self.master.add_log(f"IMSI : Scan lancé à {val}m. Matériel déployé détecté.")
        else:
            self.is_scanning = False
            self.range_slider.configure(state="normal")
            
            self.terminal.configure(state="normal")
            self.terminal.insert("1.0", "[SYSTEM] Interceptor disconnected. Frequencies offline.\n")
            self.terminal.configure(state="disabled")
            
            if hasattr(self.master, 'add_log'):
                self.master.add_log("IMSI : Désactivation du module d'interception.")