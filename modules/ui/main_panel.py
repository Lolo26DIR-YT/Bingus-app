import customtkinter as ctk
import random
import os
from modules.targets import CATEGORIES
from modules.equipment import STORE_ITEMS
from modules.ui.briefing import BriefingDialog
from modules.ui.video_player import VideoBackgroundPlayer


class HybridHackGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete=None, profile=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.target = target
        self.on_complete = on_complete
        self.profile = profile
        self.step_index = 0
        self.phase = "auto"
        
        self.total_duration = random.uniform(3, 20)
        self.start_time = None
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

        # Titre Cyber
        self.title_label = ctk.CTkLabel(
            self,
            text="Exécution du piratage automatique",
            font=ctk.CTkFont(family="JetBrains Mono", size=22, weight="bold"),
            text_color="#66fcf1"
        )
        self.title_label.pack(pady=(40, 20))

        # Texte d'étape très visible (Blanc)
        self.phase_label = ctk.CTkLabel(
            self,
            text=self.all_phases[0],
            font=ctk.CTkFont(family="JetBrains Mono", size=14, weight="normal"),
            text_color="#ffffff"
        )
        self.phase_label.pack(pady=(10, 15))

        # Barre de chargement Néon Cyan
        self.progress_bar = ctk.CTkProgressBar(
            self,
            width=500,
            height=15,
            progress_color="#66fcf1",
            fg_color="#1f2833"
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(10, 40))

        self.start_auto_phase()

    def start_auto_phase(self):
        import time
        self.start_time = time.time()
        self._update_loop()

    def _update_loop(self):
        import time
        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.total_duration, 1.0)
        self.progress_bar.set(progress)

        num_phases = len(self.all_phases) - 1
        current_step = int(progress * num_phases)
        if current_step < len(self.all_phases):
            self.phase_label.configure(text=self.all_phases[current_step])

        if progress < 1.0:
            self.after(50, self._update_loop)
        else:
            self.phase_label.configure(text=self.all_phases[-1])
            self.after(1000, self.finish_game)

    def finish_game(self):
        if self.on_complete:
            self.on_complete(True)


class MainPanel(ctk.CTkFrame):
    def __init__(self, parent, on_start_hack, on_request_log, on_show_inventory, on_toggle_sidebar, inventory=None, **kwargs):
        super().__init__(parent, fg_color="#0b0c10", **kwargs)
        self.on_start_hack = on_start_hack
        self.on_request_log = on_request_log
        self.on_show_inventory = on_show_inventory
        self.on_toggle_sidebar = on_toggle_sidebar
        self.inventory = inventory if inventory is not None else set()
        
        self.current_target = None
        self.active_game = None
        self._video_player = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Conteneur pour les pages statiques
        self.info_frame = ctk.CTkFrame(self, fg_color="#131820", border_width=1, border_color="#1f2833")
        self.info_frame.grid(row=0, column=0, sticky="nsew")
        self.info_frame.grid_rowconfigure(0, weight=1)
        self.info_frame.grid_columnconfigure(0, weight=1)

        # Bannière d'échec rouge
        self.failure_banner = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(family="JetBrains Mono", size=16, weight="bold"),
            fg_color="#ff5555",
            text_color="#ffffff",
            height=40
        )
        self.failure_banner.grid(row=1, column=0, sticky="ew", pady=(10,0))
        self.failure_banner.grid_remove()

    def show_home_page(self):
        self._reset_view()
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        home_label = ctk.CTkLabel(
            self.info_frame,
            text="SÉLECTIONNEZ UNE CIBLE DANS LA SIDEBAR POUR COMMENCER",
            font=ctk.CTkFont(family="JetBrains Mono", size=16, weight="bold"),
            text_color="#66fcf1"
        )
        home_label.grid(row=0, column=0, padx=20, pady=20)

    def show_inventory_page(self):
        self._reset_view()
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        scroll = ctk.CTkScrollableFrame(self.info_frame, fg_color="transparent")
        scroll.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            scroll, 
            text="VOTRE MATÉRIEL CYBER", 
            font=ctk.CTkFont(family="JetBrains Mono", size=18, weight="bold"),
            text_color="#66fcf1"
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 20))

        if not self.inventory:
            empty = ctk.CTkLabel(
                scroll, 
                text="Aucun équipement acheté. Visitez la boutique d'une cible pour vous équiper.",
                font=ctk.CTkFont(family="JetBrains Mono", size=13),
                text_color="#c5c6c7"
            )
            empty.grid(row=1, column=0, sticky="w")
            return

        for idx, item_name in enumerate(sorted(self.inventory)):
            item_desc = STORE_ITEMS.get(item_name, "Équipement spécialisé")
            item_frame = ctk.CTkFrame(scroll, fg_color="#1f2833", border_width=1, border_color="#45a29e")
            item_frame.grid(row=idx+1, column=0, sticky="ew", pady=5)
            item_frame.grid_columnconfigure(1, weight=1)

            lbl_name = ctk.CTkLabel(item_frame, text=f"🔧 {item_name}", font=ctk.CTkFont(family="JetBrains Mono", size=14, weight="bold"), text_color="#66fcf1")
            lbl_name.grid(row=0, column=0, padx=15, pady=10, sticky="w")

            lbl_desc = ctk.CTkLabel(item_frame, text=item_desc, font=ctk.CTkFont(family="JetBrains Mono", size=12), text_color="#c5c6c7", justify="left")
            lbl_desc.grid(row=0, column=1, padx=15, pady=10, sticky="w")

    def show_target(self, target):
        self._reset_view()
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        self.current_target = target
        self.failure_banner.grid_remove()
        self.info_frame.grid()

        scroll = ctk.CTkScrollableFrame(self.info_frame, fg_color="transparent")
        scroll.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        scroll.grid_columnconfigure(0, weight=1)

        # Nom de la Cible
        tgt_title = ctk.CTkLabel(
            scroll,
            text=target.get("name", "CIBLE INCONNUE").upper(),
            font=ctk.CTkFont(family="JetBrains Mono", size=24, weight="bold"),
            text_color="#66fcf1"
        )
        tgt_title.grid(row=0, column=0, sticky="w", pady=(0, 5))

        # IP et Distance
        target_ip = target.get('ip', 'Inconnue')
        target_distance = target.get('distance_label', 'Distance inconnue')

        lbl_meta = ctk.CTkLabel(
            scroll,
            text=f"IP: {target_ip}  |  {target_distance}",
            font=ctk.CTkFont(family="JetBrains Mono", size=12, weight="bold"),
            text_color="#45a29e"
        )
        lbl_meta.grid(row=1, column=0, sticky="w", pady=(0, 20))

        # Description / Consignes
        lbl_desc = ctk.CTkLabel(
            scroll,
            text=target.get("description", "Aucune consigne disponible pour cette cible."),
            font=ctk.CTkFont(family="JetBrains Mono", size=14),
            text_color="#c5c6c7",
            justify="left",
            wraplength=600
        )
        lbl_desc.grid(row=2, column=0, sticky="w", pady=(0, 25))

        # Analyse des systèmes de sécurité / Risques Polices
        req_frame = ctk.CTkFrame(scroll, fg_color="#1f2833", border_width=1, border_color="#45a29e")
        req_frame.grid(row=3, column=0, sticky="ew", pady=(0, 25))
        req_frame.grid_columnconfigure(0, weight=1)

        req_title = ctk.CTkLabel(req_frame, text="ANALYSE DES SYSTÈMES DE SÉCURITÉ", font=ctk.CTkFont(family="JetBrains Mono", size=13, weight="bold"), text_color="#66fcf1")
        req_title.grid(row=0, column=0, sticky="w", padx=15, pady=(12, 8))

        security_text = (
            f"• Type d'Alerte : {target.get('alert_type', 'Basse')}\n"
            f"• Difficulté Générale : {target.get('difficulty_label', 'Inconnue')}\n"
            f"• Protection Périmétrique : {target.get('defense_label', 'Aucune')}"
        )
        req_lbl = ctk.CTkLabel(req_frame, text=security_text, font=ctk.CTkFont(family="JetBrains Mono", size=13), text_color="#c5c6c7", justify="left")
        req_lbl.grid(row=1, column=0, sticky="w", padx=15, pady=(0, 15))

        # Zone des Boutons d'Action (Lancement & Boutique)
        btn_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_frame.grid(row=4, column=0, sticky="w", pady=10)

        # CORRECTION : On va chercher profile_name dans l'application parent (master) ou "Intermédiaire" par défaut
        profile = getattr(self.master, 'profile_name', 'Intermédiaire')

        hack_btn = ctk.CTkButton(
            btn_frame,
            text="INJECTER EXPLOIT",
            font=ctk.CTkFont(family="JetBrains Mono", size=14, weight="bold"),
            fg_color="#45a29e",
            hover_color="#66fcf1",
            text_color="#0b0c10",
            height=40,
            width=180,
            command=lambda: BriefingDialog(self, target, profile, self._on_briefing_result)
        )
        hack_btn.grid(row=0, column=0, padx=(0, 15))

        store_btn = ctk.CTkButton(
            btn_frame,
            text="BLACK MARKET (BOUTIQUE)",
            font=ctk.CTkFont(family="JetBrains Mono", size=14, weight="bold"),
            fg_color="#1f2833",
            hover_color="#45a29e",
            text_color="#66fcf1",
            height=40,
            width=220,
            command=self.show_store_page
        )
        store_btn.grid(row=0, column=1)

    def show_store_page(self):
        if not self.current_target:
            return
        self._reset_view()
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        scroll = ctk.CTkScrollableFrame(self.info_frame, fg_color="transparent")
        scroll.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        target_name = self.current_target.get('name', 'Cible').upper()
        title = ctk.CTkLabel(
            scroll, 
            text=f"BLACK MARKET — MATÉRIEL RECOMMANDÉ POUR {target_name}", 
            font=ctk.CTkFont(family="JetBrains Mono", size=16, weight="bold"),
            text_color="#66fcf1"
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 20))

        items_to_show = ["WiFi Pineapple", "Signal Analyser", "Antenna Extension", "SCADA Kit", "0-Day Kit"]
        
        for idx, item_name in enumerate(items_to_show):
            item_desc = STORE_ITEMS.get(item_name, "Équipement spécialisé pour les opérations réseau.")
            item_frame = ctk.CTkFrame(scroll, fg_color="#1f2833", border_width=1, border_color="#1f2833")
            item_frame.grid(row=idx+1, column=0, sticky="ew", pady=5)
            item_frame.grid_columnconfigure(1, weight=1)

            lbl_name = ctk.CTkLabel(item_frame, text=item_name, font=ctk.CTkFont(family="JetBrains Mono", size=14, weight="bold"), text_color="#66fcf1")
            lbl_name.grid(row=0, column=0, padx=15, pady=15, sticky="w")

            lbl_desc = ctk.CTkLabel(item_frame, text=item_desc, font=ctk.CTkFont(family="JetBrains Mono", size=12), text_color="#c5c6c7", justify="left", wraplength=400)
            lbl_desc.grid(row=0, column=1, padx=15, pady=15, sticky="w")

            if item_name in self.inventory:
                btn_buy = ctk.CTkButton(item_frame, text="ACQUIS", state="disabled", fg_color="#131820", text_color="#45a29e", width=100)
            else:
                btn_buy = ctk.CTkButton(
                    item_frame, 
                    text="ACHETER", 
                    fg_color="#45a29e", 
                    hover_color="#66fcf1", 
                    text_color="#0b0c10", 
                    width=100,
                    command=lambda name=item_name: self.buy_item(name)
                )
            btn_buy.grid(row=0, column=2, padx=15, pady=15, sticky="e")

    def buy_item(self, item_name):
        self.inventory.add(item_name)
        self.on_request_log(f"Équipement acheté : {item_name}")
        self.show_store_page()

    def start_hack(self, target, profile):
        self._reset_view()
        self.current_target = target
        self.failure_banner.grid_remove()
        self.on_toggle_sidebar(False)

        self.info_frame.grid_remove()

        self.active_game = HybridHackGame(self, target, on_complete=self._on_hack_complete, profile=profile)
        self.active_game.grid(row=0, column=0, sticky="nsew")

    def _on_hack_complete(self, success):
        self.on_toggle_sidebar(True)
        if self.active_game:
            self.active_game.destroy()
            self.active_game = None

        self.info_frame.grid()

        if success:
            self.show_target(self.current_target)
            self.on_request_log(f"Hack réussi sur : {self.current_target.get('name', 'Cible')}")
            
            video_path = os.path.join("resources", "videos", "success_loop.mp4")
            if os.path.exists(video_path):
                self._video_player = VideoBackgroundPlayer(self, video_path)
                self._video_player.play()
                self.after(6000, self._video_player.stop)
        else:
            self.on_request_log(f"Hack échoué : {self.current_target.get('name', 'Cible')}")

    def _on_briefing_result(self, proceed):
        if proceed and self.current_target:
            profile = getattr(self.master, 'profile_name', 'Intermédiaire')
            self.start_hack(self.current_target, profile)

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

    def _reset_view(self):
        if self.active_game:
            self.active_game.destroy()
            self.active_game = None

    def _alert_type(self, target):
        if target.get("alert_type"):
            return target["alert_type"]
        return "Basse"