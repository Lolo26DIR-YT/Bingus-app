import customtkinter as ctk
import random
import string

class BruteForcePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Liste des vitesses imposées (essais par seconde)
        self.SPEEDS = [1, 2, 3, 5, 10, 20, 30, 50, 100, 500]
        self.is_active = False

        # Dictionnaire de mots RP pour générer de faux mots de passe réalistes
        self.FAKE_WORDS = ["admin", "password", "root", "cyber", "matrix", "gta", "lolo26", "shadow", "secure", "hack"]

        # --- TITRE DE LA PAGE ---
        self.title_label = ctk.CTkLabel(
            self, 
            text="💻 Injecteur Brute-Force", 
            font=ctk.CTkFont(family="Courier", size=24, weight="bold"),
            text_color="#66fcf1"
        )
        self.title_label.pack(pady=(20, 10))

        # --- CONSOLE DES ESSAIS (CHAMPS SPÉCIAL STABLE) ---
        self.console_frame = ctk.CTkFrame(self, fg_color="#131820", border_width=1, border_color="#45a29e")
        self.console_frame.pack(pady=15, padx=20, fill="x")

        # Conteneur interne pour aligner les deux textes sans bouger
        self.display_container = ctk.CTkFrame(self.console_frame, fg_color="transparent")
        self.display_container.pack(pady=10, expand=True)

        # 1. Le préfixe fixe (qui ne bouge JAMAIS)
        self.prefix_label = ctk.CTkLabel(
            self.display_container, 
            text="STATUS : ", 
            font=ctk.CTkFont(family="Courier", size=18, weight="bold"),
            text_color="#45a29e"
        )
        self.prefix_label.pack(side="left")

        # 2. La valeur variable (seuls les mots de passe changent ici)
        self.password_label = ctk.CTkLabel(
            self.display_container, 
            text="SYSTEME EN ATTENTE", 
            font=ctk.CTkFont(family="Courier", size=18, weight="bold"),
            text_color="#45a29e"
        )
        self.password_label.pack(side="left")

        # --- SECTION RÉGLETTE (VITESSE) ---
        self.speed_label = ctk.CTkLabel(
            self, 
            text="Vitesse d'injection : 10 essais / sec", 
            font=ctk.CTkFont(family="Courier", size=14),
            text_color="#c5c6c7"
        )
        self.speed_label.pack(pady=(20, 5))

        # Configuration du curseur calé sur les index de notre liste (0 à 9)
        self.speed_slider = ctk.CTkSlider(
            self, 
            from_=0, 
            to=len(self.SPEEDS) - 1, 
            number_of_steps=len(self.SPEEDS) - 1,
            command=self.update_speed,
            button_color="#45a29e",
            button_hover_color="#66fcf1",
            progress_color="#45a29e"
        )
        self.speed_slider.set(4) 
        self.speed_slider.pack(pady=10, padx=40, fill="x")

        # --- TOGGLE D'ACTIVATION (SWITCH) ---
        self.attack_switch = ctk.CTkSwitch(
            self, 
            text="Lancer l'attaque de dictionnaire", 
            command=self.toggle_attack, 
            font=ctk.CTkFont(family="Courier", size=16, weight="bold"),
            text_color="#66fcf1",
            progress_color="#FF4C4C"
        )
        self.attack_switch.pack(pady=30)

    def update_speed(self, value):
        """Met à jour l'affichage de la vitesse selon la réglette."""
        index = int(round(float(value)))
        speed = self.SPEEDS[index]
        self.speed_label.configure(text=f"Vitesse d'injection : {speed} essais / sec")

    def generate_fake_password(self):
        """Fabrique un faux mot de passe semi-aléatoire pour l'effet visuel."""
        if random.choice([True, False]):
            return f"{random.choice(self.FAKE_WORDS)}{random.randint(10, 999)}"
        else:
            chars = string.ascii_letters + string.digits
            return "".join(random.choice(chars) for _ in range(random.randint(6, 12)))

    def run_injection(self):
        """Boucle d'affichage des mots de passe calée sur la vitesse choisie."""
        if not self.is_active:
            return

        index = int(round(self.speed_slider.get()))
        speed = self.SPEEDS[index]

        # On change uniquement le texte variable et sa couleur
        fake_pass = self.generate_fake_password()
        self.prefix_label.configure(text="TRYING : ", text_color="#ffb703")
        self.password_label.configure(text=fake_pass, text_color="#ffb703")

        # Calcul de l'intervalle en millisecondes pour respecter les essais par seconde
        interval = max(10, int(1000 / speed))
        
        # Relance la boucle
        self.after(interval, self.run_injection)

    def toggle_attack(self):
        """Active l'attaque, bloque le curseur et envoie les logs."""
        index = int(round(self.speed_slider.get()))
        speed = self.SPEEDS[index]

        if self.attack_switch.get() == 1:
            self.is_active = True
            self.speed_slider.configure(state="disabled")
            self.run_injection()
            
            if hasattr(self.master, 'add_log'):
                self.master.add_log(f"BRUTE-FORCE : Attaque initialisée à {speed} requêtes/seconde.")
        else:
            self.is_active = False
            self.speed_slider.configure(state="normal")
            
            # Reset stable de l'affichage en cas d'arrêt
            self.prefix_label.configure(text="STATUS : ", text_color="#FF4C4C")
            self.password_label.configure(text="ATTACK ABORTED", text_color="#FF4C4C")
            
            if hasattr(self.master, 'add_log'):
                self.master.add_log("BRUTE-FORCE : Signal d'arrêt envoyé. Fin du traitement.")