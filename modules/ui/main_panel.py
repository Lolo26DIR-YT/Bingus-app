import customtkinter as ctk
import random
import os
from modules.targets import CATEGORIES
from modules.ui.briefing import BriefingDialog
from modules.ui.video_player import VideoBackgroundPlayer


class HybridHackGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.target = target
        self.on_complete = on_complete
        self.step_index = 0
        self.phase = "auto"

        base_duration = target.get("duration", 25)
        self.total_duration = base_duration + 5 
        self.remaining_seconds = base_duration + 5

        
        self.total_duration = target.get("duration", 30)
        self.remaining_seconds = self.total_duration

        # --- CALCUL DYNAMIQUE DU DÉLAI ---
        self.all_phases = [
            f"Analyseur réseau passif de {target.get('name', 'Cible')} en cours...",
            "Collecte des métadonnées en arrière-plan...",
            "Établissement du relais sécurisé...",
            "Injection de payload personnalisé...",
            "Contournement des pare-feu détecté...",
            "Extraction des données d'authentification...",
            "Installation de la porte dérobée...",
            "Suppression des logs d'accès...",
            "Finalisation du tunnel sécurisé...",
            "Vérification des traces résiduelles...",
            "Hack terminé avec succès!",
        ]
        
        total_steps = len(self.all_phases) - 1
        target_duration = max(target.get("duration", 30), 1)
        self.step_delay = int((target_duration * 1000) / total_steps)

        # Configuration de la grille
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Titre Cyber
        self.title_label = ctk.CTkLabel(
            self, 
            text=f"PIRATAGE : {target.get('name', 'Cible').upper()}", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            text_color="#66fcf1"
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        # Zone d'affichage de la console
        self.console_box = ctk.CTkTextbox(self, fg_color="#0b0c10", text_color="#45a29e", font=ctk.CTkFont(family="Courier", size=13), corner_radius=8)
        self.console_box.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="nsew")

        # --- LABEL DU MINUTEUR (C'est lui qui manquait !) ---
        self.timer_label = ctk.CTkLabel(self, text="Temps estimé : --s", text_color="#66fcf1", font=ctk.CTkFont(size=12))
        self.timer_label.grid(row=2, column=0, padx=20, pady=(0, 5), sticky="e")

        # Barre de progression
        self.progress_bar = ctk.CTkProgressBar(self, progress_color="#66fcf1", fg_color="#1f2833")
        self.progress_bar.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="ew")
        self.progress_bar.set(0)

        # Bouton d'action
        self.action_button = ctk.CTkButton(
            self, 
            text="INITIALISATION...", 
            font=ctk.CTkFont(weight="bold"),
            fg_color="#45a29e", 
            hover_color="#66fcf1", 
            text_color="#0b0c10",
            height=40,
            command=self.on_action_click
        )
        self.action_button.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Écoute de la touche Entrée
        self.winfo_toplevel().bind("<Return>", self.on_enter_pressed)

        # Lancement automatique (maintenant que timer_label existe, ça ne plantera plus)
        self.start_auto_phase()
        self.update_timer()

    def update_timer(self):
        if self.phase == "auto":
            if self.remaining_seconds > 0:
                self.remaining_seconds -= 1
                self.timer_label.configure(text=f"Temps restant : {self.remaining_seconds}s")
                self.after(1000, self.update_timer)
            else:
                self.timer_label.configure(text="Temps écoulé !")

    def start_auto_phase(self):
        if self.step_index < len(self.all_phases) - 1:
            # --- Calcul du temps restant ---
            steps_left = (len(self.all_phases) - 1) - self.step_index
            seconds_left = int(steps_left * (self.step_delay / 1000))
            self.timer_label.configure(text=f"Temps restant : {seconds_left}s")
            # -------------------------------

            current_text = self.all_phases[self.step_index]
            self.console_box.insert("end", f"[SYSTEM] {current_text}\n")
            self.console_box.see("end")
            
            progress_val = (self.step_index + 1) / (len(self.all_phases) - 1)
            self.progress_bar.set(progress_val)
            
            self.step_index += 1
            self.after(self.step_delay, self.start_auto_phase)
        else:
            self.timer_label.configure(text="SÉQUENCE TERMINÉE")
            self.phase = "manual"
            self.progress_bar.set(0.9)
            self.action_button.configure(text=f"APPUYER SUR ENTRÉE POUR INJECTER LE CODE FINAL")
            self.console_box.insert("end", "\n[ATTENTION] Séquence finale en attente de validation manuelle...\n")
            self.console_box.see("end")

    def on_enter_pressed(self, event):
        self.on_action_click()

    def on_action_click(self):
        if self.phase == "manual":
            roll = random.randint(1, 240)

            # 1. BLOCAGE SYSTÈME (Rouge)
            if roll <= 15:
                self.phase = "failed_blocked"
                self.progress_bar.set(0.0)
                self.progress_bar.configure(progress_color="#ff4d4d")
                
                self.console_box.insert("end", "\n[CRITICAL ERROR] CONTRE-MESURE DETECTEE !\n", "red")
                self.console_box.insert("end", "[SYSTEM] Système verrouillé. Terminal hors-ligne.\n", "red")
                self.console_box.see("end")
                
                self.action_button.configure(text="SYSTÈME BLOQUÉ - FERMER", fg_color="#ff4d4d")
                if self.on_complete:
                    self.on_complete(False)

            # 2. ALERTE FDO (Bleu)
            elif roll <= 15 + 12:
                self.phase = "failed_fdo"
                self.progress_bar.set(0.0)
                self.progress_bar.configure(progress_color="#00d2d3")
                
                self.console_box.insert("end", "\n[ALERTE] TRANSMISSION COMPROMISE !\n", "blue")
                self.console_box.insert("end", "[INFO] Forces de l'ordre alertées.\n", "blue")
                
                # --- FORCER L'AFFICHAGE ---
                self.update_idletasks() # Recalcule la mise en page
                self.console_box.see("end") # Scrolle vers le bas
                
                self.action_button.configure(text="ALERTE FDO - QUITTER", fg_color="#00d2d3")
                
                # Affichage de la bannière
                if self.master and hasattr(self.master.master, "_show_failure_banner"):
                    self.master.master._show_failure_banner(self.target)
                    
                if self.on_complete:
                    self.on_complete(False, reason="FDO")

            # 3. ÉCHEC STANDARD (Orange)
            elif roll <= 15 + 12 + 48:
                self.phase = "failed_standard"
                self.progress_bar.set(0.0)
                self.progress_bar.configure(progress_color="#ff9f43")
                
                self.console_box.insert("end", "\n[ÉCHEC] INJECTION REJETÉE par le pare-feu.\n", "orange")
                self.console_box.insert("end", "[RETRY] Connexion perdue.\n", "orange")
                self.console_box.see("end")
                
                self.action_button.configure(text="ÉCHEC DU HACK - FERMER", fg_color="#ff9f43")
                if self.on_complete:
                    self.on_complete(False)

            # 4. SUCCÈS (Vert)
            else:
                self.phase = "complete"
                self.progress_bar.set(1.0)
                self.console_box.insert("end", "\n[SUCCÈS] Injection validée ! Accès total accordé.\n", "green")
                self.console_box.see("end")
                self.action_button.configure(text="FERMER L'INTERFACE", fg_color="#28a745")
                if self.on_complete:
                    self.on_complete(True)

        # Gestion de la fermeture (clic sur le bouton après résultat)
        elif self.phase in ["complete", "failed_standard", "failed_blocked", "failed_fdo"]:
            # On retire la bannière de police si elle est affichée
            if self.master and hasattr(self.master.master, "failure_banner"):
                self.master.master.failure_banner.grid_remove()
            
            # Nettoyage clavier et destruction
            self.winfo_toplevel().unbind("<Return>")
            self.destroy()
class MainPanel(ctk.CTkFrame):
    def __init__(self, parent, on_request_log=None, on_start_hack=None, on_toggle_sidebar=None, **kwargs):
        super().__init__(parent, fg_color="#131820", corner_radius=0, **kwargs)
        self.on_request_log = on_request_log
        self.on_start_hack = on_start_hack
        self.on_toggle_sidebar = on_toggle_sidebar
        self.current_target = None
        self._video_player = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)  
        self.rowconfigure(1, weight=1)  
        self.rowconfigure(2, weight=0)  

        # 1. Bannière d'alerte Police
        self.failure_banner = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#721c24",
            text_color="#f8d7da",
            height=35,
            corner_radius=6
        )
        self.failure_banner.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="ew")
        self.failure_banner.grid_remove()
        

        # 2. Zone de Contenu Dynamique
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)

        # 3. Bas de page épuré
        self.setup_profile_footer()

        # Affichage de l'écran d'accueil de base
        self.show_welcome_screen()

    def setup_profile_footer(self):
        self.footer_frame = ctk.CTkFrame(self, fg_color="#0b0c10", height=70, corner_radius=10)
        self.footer_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        self.footer_frame.grid_propagate(False)
        
        self.footer_frame.columnconfigure(0, weight=1)
        self.footer_frame.rowconfigure(0, weight=1)

        self.briefing_btn = ctk.CTkButton(
            self.footer_frame,
            text="OUVRIR LE BRIEFING OPÉRATIONNEL",
            font=ctk.CTkFont(weight="bold", size=13),
            fg_color="#45a29e",
            hover_color="#66fcf1",
            text_color="#0b0c10",
            state="disabled",
            height=40,
            command=self.trigger_briefing
        )
        self.briefing_btn.grid(row=0, column=0, padx=20, sticky="ew")

    def show_home_page(self):
        self.show_welcome_screen()

    def show_welcome_screen(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        welcome_label = ctk.CTkLabel(
            self.content_frame,
            text="SÉLECTIONNEZ UNE CIBLE DANS LA SIDEBAR POUR COMMENCER",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#45a29e"
        )
        welcome_label.grid(row=0, column=0, padx=20, pady=20)
        
        if hasattr(self, 'briefing_btn') and self.briefing_btn.winfo_exists():
            self.briefing_btn.configure(state="disabled")

    def show_target(self, target):
        self.current_target = target
        # ICI : On cache la bannière dès qu'on sélectionne une nouvelle cible
        self.failure_banner.grid_remove() 
        
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        info_box = ctk.CTkFrame(self.content_frame, fg_color="#0b0c10", corner_radius=12)
        info_box.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        info_box.columnconfigure(0, weight=1)

        title = ctk.CTkLabel(info_box, text=target.get("name", "Cible"), font=ctk.CTkFont(size=22, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, pady=(30, 15))

        desc = ctk.CTkLabel(info_box, text=target.get("rp_description", ""), font=ctk.CTkFont(size=13), text_color="#c5c6c7", wraplength=400, height=50)
        desc.grid(row=1, column=0, pady=10, padx=20)

        self.briefing_btn.configure(state="normal")

    def load_target(self, target):
        self.show_target(target)

    def trigger_briefing(self):
        if self.current_target:
            dialog = BriefingDialog(self, self.current_target, "Standard", self._on_briefing_result)
            dialog.grab_set()

    def start_hack(self, target, profile="Standard"):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        game = HybridHackGame(self.content_frame, target, on_complete=self.on_hack_complete)
        game.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        if self.on_request_log:
            self.on_request_log(f"Initialisation de l'attaque sur {target.get('name')}")
        if self.on_start_hack:
            self.on_start_hack(target, profile)

    # Ajoute "=None" ici pour éviter l'erreur "reason is not defined"
    def on_hack_complete(self, success, reason=None):
        if success:
            if self.on_request_log:
                self.on_request_log(f"Hack réussi avec succès sur : {self.current_target.get('name', 'Cible')}")
            
            video_path = os.path.join("resources", "videos", "success_loop.mp4")
            if os.path.exists(video_path):
                self._video_player = VideoBackgroundPlayer(self, video_path)
                self._video_player.play()
                self.after(6000, self._video_player.stop)
        else:
            # On vérifie la raison ici
            if reason == "FDO":
                self.on_request_log(f"!!! ALERTE FDO !!! Trace activée sur {self.current_target.get('name')}")
            else:
                self.on_request_log(f"Hack échoué : {self.current_target.get('name', 'Cible')}")

    def _on_briefing_result(self, proceed):
        if proceed and self.current_target:
            self.start_hack(self.current_target)

    def _show_failure_banner(self, target):
        grade = self._police_grade(target)
        self.failure_banner.configure(text=f"LA POLICE {grade.upper()} A ÉTÉ INFORMÉE DU PIRATAGE")
        self.failure_banner.grid()

    def _police_grade(self, target):
        alert = self._alert_type(target).lower()
        if "locale" in alert:
            return "locale"
        if "étatique" in alert or "ethatique" in alert:
            return "étatique"
        if "fédérale" in alert or "federale" in alert:
            return "fédérale"
        return "locale"

    def _alert_type(self, target):
        risk = target.get("risk", 1)
        if risk <= 2:
            return "Locale"
        elif risk <= 4:
            return "Étatique"
        else:
            return "Fédérale"