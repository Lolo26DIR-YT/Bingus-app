import customtkinter as ctk
from modules.targets import CATEGORIES
from modules.equipment import STORE_ITEMS
from modules.ui.briefing import BriefingDialog
from modules.minigames.categories.manual import ManualHackDialog
from modules.minigames.core import MINI_GAME_CLASSES, HybridHackGame


class HybridHackGame(ctk.CTkFrame):
    def __init__(self, parent, target, manual_game_class, on_complete, profile=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.target = target
        self.manual_game_class = manual_game_class
        self.on_complete = on_complete
        self.profile = profile
        self.step_index = 0
        self.phase = "auto"
        self.auto_phases = [
            f"Analyse passive de {target['name']}...",
            "Collecte des métadonnées en arrière-plan...",
            "Établissement du relais sécurisé...",
        ]
        self.final_phases = [
            "Finalisation du tunnel sécurisé...",
            "Vérification des traces...",
        ]
        self.current_phases = self.auto_phases

        self.columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Phase automatique du hack", font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        self.auto_status = ctk.CTkLabel(self, text="Lancement de la phase automatique...", text_color="#c5c6c7", wraplength=760, justify="left")
        self.auto_status.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))

        self.auto_progress = ctk.CTkProgressBar(self)
        self.auto_progress.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.auto_progress.set(0.0)

        self.manual_hint = ctk.CTkLabel(self, text="Une phase manuelle sera nécessaire, la fenêtre s'ouvrira automatiquement.", text_color="#f1fa8c", wraplength=760, justify="left")
        self.manual_hint.grid(row=3, column=0, sticky="w", padx=16, pady=(0, 12))

        self.after(500, self._advance_auto_phase)

    def _advance_auto_phase(self):
        if self.step_index >= len(self.current_phases):
            if self.phase == "auto":
                self.auto_status.configure(text="Phase automatique terminée. Ouverture de la page manuelle...")
                self.auto_progress.set(1.0)
                self.after(800, self._open_manual_page)
                return

            self.auto_progress.set(1.0)
            self.auto_status.configure(text="Hack terminé. Traitement finalisé.")
            self.after(400, lambda: self.on_complete(True))
            return

        self.auto_status.configure(text=self.current_phases[self.step_index])
        self.step_index += 1
        self.auto_progress.set(self.step_index / len(self.current_phases))
        self.after(1100, self._advance_auto_phase)

    def _open_manual_page(self):
        self.manual_hint.configure(text="La page de hack manuel est ouverte. Validez avec le bouton Fait une fois terminé.")
        self.manual_window = ManualHackDialog(self, self.target, self.manual_game_class, self._manual_finished, profile=self.profile)
        self.manual_window.grab_set()

    def _manual_finished(self, success):
        if not success:
            self.on_complete(False)
            return

        self.phase = "final"
        self.current_phases = self.final_phases
        self.step_index = 0
        self.auto_status.configure(text="Reprise de la phase automatique finale...")
        self.auto_progress.set(0.0)
        self.manual_hint.configure(text="La phase manuelle est terminée. Finalisation en cours...")
        self.after(800, self._advance_auto_phase)


class MainPanel(ctk.CTkFrame):
    def __init__(self, parent, on_start_hack, on_request_log, on_show_inventory=None, on_toggle_sidebar=None, inventory=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_start_hack = on_start_hack
        self.on_request_log = on_request_log
        self.on_show_inventory = on_show_inventory
        self.on_toggle_sidebar = on_toggle_sidebar
        self.inventory = inventory if inventory is not None else set()
        self.current_target = None
        self.current_profile = "Intermédiaire"
        self.active_game = None
        self.selected_store_item = None
        self.selected_hack_menu_target = None
        self.checklist_vars = {}
        self.current_view = "home"

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.home_page = ctk.CTkFrame(self, fg_color="#0b0c10")
        self.reference_page = ctk.CTkFrame(self, fg_color="#0b0c10")
        self.hack_menu_page = ctk.CTkFrame(self, fg_color="#0b0c10")
        self.store_page = ctk.CTkFrame(self, fg_color="#0b0c10")
        self.inventory_page = ctk.CTkFrame(self, fg_color="#0b0c10")
        self.checklist_page = ctk.CTkFrame(self, fg_color="#0b0c10")
        self.hack_page_frame = ctk.CTkFrame(self, fg_color="#0b0c10")

        self._build_home_page()
        self._build_reference_page()
        self._build_hack_menu_page()
        self._build_store_page()
        self._build_inventory_page()
        self._build_checklist_page()
        self._build_hack_page_frame()

        self.show_home_page()

    def _hide_all_pages(self):
        for frame in [
            self.home_page,
            self.reference_page,
            self.hack_menu_page,
            self.store_page,
            self.inventory_page,
            self.checklist_page,
            self.hack_page_frame,
        ]:
            frame.grid_remove()

    def _build_home_page(self):
        self.home_page.columnconfigure(0, weight=1)
        self.home_page.rowconfigure((0, 1, 2, 3, 4), weight=1)

        title = ctk.CTkLabel(self.home_page, text="Accueil des hacks", font=ctk.CTkFont(size=24, weight="bold"), text_color="#7dc4e4")
        title.grid(row=0, column=0, sticky="n", padx=20, pady=(24, 12))

        description = ctk.CTkLabel(
            self.home_page,
            text="Choisissez une action : consulter les fiches techniques, accéder au menu de hacks, gérer la checklist ou acheter de l'équipement.",
            wraplength=760,
            justify="center",
            text_color="#b0bcc5",
        )
        description.grid(row=1, column=0, sticky="n", padx=32, pady=(0, 16))

        button_frame = ctk.CTkFrame(self.home_page, fg_color="#131820")
        button_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=12)
        button_frame.columnconfigure((0, 1), weight=1)
        button_frame.rowconfigure(0, weight=1)

        reference_button = ctk.CTkButton(button_frame, text="Fiches techniques", command=self.show_reference_page, fg_color="#1f2833")
        reference_button.grid(row=0, column=0, sticky="nsew", padx=(12, 6), pady=12)
        hack_menu_button = ctk.CTkButton(button_frame, text="Menu hacks", command=self.show_hack_menu_page, fg_color="#45a29e")
        hack_menu_button.grid(row=0, column=1, sticky="nsew", padx=(6, 12), pady=12)

        button_frame2 = ctk.CTkFrame(self.home_page, fg_color="#131820")
        button_frame2.grid(row=3, column=0, sticky="nsew", padx=20, pady=12)
        button_frame2.columnconfigure((0, 1), weight=1)
        button_frame2.rowconfigure(0, weight=1)

        shop_button = ctk.CTkButton(button_frame2, text="Achat d'équipement", command=self.show_store_page, fg_color="#66fcf1")
        shop_button.grid(row=0, column=0, sticky="nsew", padx=(12, 6), pady=12)
        checklist_button = ctk.CTkButton(button_frame2, text="Checklist mission", command=self.show_checklist_page, fg_color="#45a29e")
        checklist_button.grid(row=0, column=1, sticky="nsew", padx=(6, 12), pady=12)

        footer = ctk.CTkLabel(
            self.home_page,
            text="Utilisez la checklist pour cocher les hacks prévus et connaître les outils requis.",
            wraplength=760,
            justify="center",
            text_color="#b0bcc5",
        )
        footer.grid(row=4, column=0, sticky="n", padx=32, pady=(12, 24))

    def _build_reference_page(self):
        self.reference_page.columnconfigure(0, weight=1)
        self.reference_content = ctk.CTkScrollableFrame(self.reference_page, fg_color="#131820")
        self.reference_content.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        self.reference_content.columnconfigure(0, weight=1)

    def _build_hack_menu_page(self):
        self.hack_menu_page.columnconfigure((0, 1), weight=1)
        self.hack_menu_page.rowconfigure(0, weight=1)

        self.hack_menu_list = ctk.CTkScrollableFrame(self.hack_menu_page, fg_color="#131820")
        self.hack_menu_list.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)
        self.hack_menu_list.columnconfigure(0, weight=1)

        details_frame = ctk.CTkFrame(self.hack_menu_page, fg_color="#131820")
        details_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=16)
        details_frame.columnconfigure(0, weight=1)

        self.hack_menu_title = ctk.CTkLabel(details_frame, text="Sélectionnez un hack pour voir sa fiche.", font=ctk.CTkFont(size=18, weight="bold"), text_color="#7dc4e4")
        self.hack_menu_title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 12))

        self.hack_menu_details = ctk.CTkLabel(details_frame, text="", wraplength=520, justify="left", text_color="#b0bcc5")
        self.hack_menu_details.grid(row=1, column=0, sticky="nw", padx=16, pady=(0, 12))

        self.hack_menu_launch_button = ctk.CTkButton(details_frame, text="Lancer le hack", command=self._launch_selected_hack, fg_color="#45a29e")
        self.hack_menu_launch_button.grid(row=2, column=0, sticky="ew", padx=16, pady=(8, 16))
        self.hack_menu_launch_button.configure(state="disabled")

    def _build_store_page(self):
        self.store_page.columnconfigure((0, 1), weight=1)
        self.store_page.rowconfigure(0, weight=0)
        self.store_page.rowconfigure(1, weight=1)

        self.store_search_var = ctk.StringVar(value="")

        search_frame = ctk.CTkFrame(self.store_page, fg_color="#131820")
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 4))
        search_frame.columnconfigure((0, 1), weight=1)

        self.store_search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Rechercher un équipement...",
            textvariable=self.store_search_var,
            fg_color="#0b0c10",
            text_color="#c5c6c7",
        )
        self.store_search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8), pady=8)
        self.store_search_entry.bind("<KeyRelease>", lambda event: self._render_store_items())

        clear_button = ctk.CTkButton(search_frame, text="Effacer", command=self._clear_store_search, fg_color="#1f2833")
        clear_button.grid(row=0, column=1, sticky="ew", padx=(0, 0), pady=8)

        sort_label = ctk.CTkLabel(search_frame, text="Trié par prix croissant", text_color="#7fbdd1")
        sort_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=(0, 8), pady=(0, 4))

        self.store_list = ctk.CTkScrollableFrame(self.store_page, fg_color="#131820")
        self.store_list.grid(row=1, column=0, sticky="nsew", padx=(16, 8), pady=16)
        self.store_list.columnconfigure(0, weight=1)

        self.store_detail_frame = ctk.CTkFrame(self.store_page, fg_color="#131820")
        self.store_detail_frame.grid(row=1, column=1, sticky="nsew", padx=(8, 16), pady=16)
        self.store_detail_frame.columnconfigure(0, weight=1)

        self.store_item_name = ctk.CTkLabel(self.store_detail_frame, text="Sélectionnez un équipement.", font=ctk.CTkFont(size=18, weight="bold"), text_color="#7dc4e4")
        self.store_item_name.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 12))

        self.store_item_description = ctk.CTkLabel(self.store_detail_frame, text="", wraplength=520, justify="left", text_color="#b0bcc5")
        self.store_item_description.grid(row=1, column=0, sticky="nw", padx=16, pady=(0, 12))

        self.store_item_details = ctk.CTkLabel(self.store_detail_frame, text="", wraplength=520, justify="left", text_color="#7fbdd1")
        self.store_item_details.grid(row=2, column=0, sticky="nw", padx=16, pady=(0, 12))

        self.store_item_price = ctk.CTkLabel(self.store_detail_frame, text="", text_color="#7fd6a6")
        self.store_item_price.grid(row=3, column=0, sticky="w", padx=16, pady=(0, 12))

        self.store_buy_button = ctk.CTkButton(self.store_detail_frame, text="Acheter", command=self._purchase_selected_item, fg_color="#45a29e")
        self.store_buy_button.grid(row=4, column=0, sticky="ew", padx=16, pady=(8, 0))

        self.store_purchase_status = ctk.CTkLabel(self.store_detail_frame, text="", wraplength=520, justify="left", text_color="#b0bcc5")
        self.store_purchase_status.grid(row=5, column=0, sticky="w", padx=16, pady=(8, 16))

    def _build_inventory_page(self):
        self.inventory_page.columnconfigure(0, weight=1)
        self.inventory_page.rowconfigure(0, weight=1)
        self.inventory_page.rowconfigure(1, weight=0)

        self.inventory_content = ctk.CTkScrollableFrame(self.inventory_page, fg_color="#131820")
        self.inventory_content.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        self.inventory_content.columnconfigure(0, weight=1)

        self.inventory_status_label = ctk.CTkLabel(
            self.inventory_page,
            text="",
            wraplength=760,
            justify="left",
            text_color="#8be9fd",
        )
        self.inventory_status_label.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 16))

    def _build_checklist_page(self):
        self.checklist_page.columnconfigure(0, weight=1)
        self.checklist_page.rowconfigure((0, 1, 2), weight=1)

        title = ctk.CTkLabel(self.checklist_page, text="Checklist de mission", font=ctk.CTkFont(size=24, weight="bold"), text_color="#7dc4e4")
        title.grid(row=0, column=0, sticky="n", padx=20, pady=(24, 12))

        self.checklist_frame = ctk.CTkScrollableFrame(self.checklist_page, fg_color="#131820")
        self.checklist_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 12))
        self.checklist_frame.columnconfigure(0, weight=1)

        self.checklist_summary = ctk.CTkLabel(
            self.checklist_page,
            text="Sélectionnez un ou plusieurs hacks pour voir les outils requis.",
            wraplength=760,
            justify="left",
            text_color="#b0bcc5",
        )
        self.checklist_summary.grid(row=2, column=0, sticky="ew", padx=24, pady=(8, 24))

    def _build_hack_page_frame(self):
        self.hack_page_frame.columnconfigure(0, weight=1)
        self.hack_page_frame.rowconfigure(5, weight=1)

        self.title_label = ctk.CTkLabel(self.hack_page_frame, text="Bingus Hack Simulator", font=ctk.CTkFont(size=22, weight="bold"), text_color="#66fcf1")
        self.title_label.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        self.failure_banner = ctk.CTkLabel(self.hack_page_frame, text="", fg_color="#ff5555", text_color="#ffffff", corner_radius=10)
        self.failure_banner.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.failure_banner.grid_remove()

        self.summary_frame = ctk.CTkFrame(self.hack_page_frame, fg_color="#0b0f16")
        self.summary_frame.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.summary_frame.columnconfigure((0, 1), weight=1)

        self.target_name = ctk.CTkLabel(self.summary_frame, text="Aucune cible sélectionnée.", font=ctk.CTkFont(size=18, weight="bold"), text_color="#d3d7db")
        self.target_name.grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=12)

        self.distance_label = ctk.CTkLabel(self.summary_frame, text="", text_color="#7dc4e4")
        self.distance_label.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))
        self.risk_label = ctk.CTkLabel(self.summary_frame, text="", text_color="#ffb86c")
        self.risk_label.grid(row=1, column=1, sticky="e", padx=16, pady=(0, 8))

        self.alert_label = ctk.CTkLabel(self.summary_frame, text="", text_color="#ff5555")
        self.alert_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 8))

        self.tools_label = ctk.CTkLabel(self.summary_frame, text="", wraplength=720, justify="left", text_color="#b0bcc5")
        self.tools_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 12))

        self.hint_label = ctk.CTkLabel(self.summary_frame, text="", wraplength=720, justify="left", text_color="#7fbdd1")
        self.hint_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 8))

        self.button_frame = ctk.CTkFrame(self.hack_page_frame, fg_color="#0b0f16")
        self.button_frame.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.button_frame.columnconfigure((0, 1), weight=1)

        self.brief_button = ctk.CTkButton(self.button_frame, text="Briefing", command=self.show_briefing, fg_color="#1f2833")
        self.brief_button.grid(row=0, column=0, sticky="ew", padx=(16, 8), pady=12)

        self.start_button = ctk.CTkButton(self.button_frame, text="Lancer le hack", command=self.request_start_hack, fg_color="#45a29e")
        self.start_button.grid(row=0, column=1, sticky="ew", padx=(8, 16), pady=12)

        self.status_label = ctk.CTkLabel(self.hack_page_frame, text="Statut : En attente", text_color="#c5c6c7")
        self.status_label.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 12))

        self.game_area = ctk.CTkFrame(self.hack_page_frame, fg_color="#0b0f16")
        self.game_area.grid(row=5, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.game_area.columnconfigure(0, weight=1)
        self.game_area.rowconfigure(0, weight=1)

    def show_home_page(self):
        self._hide_all_pages()
        if self.on_toggle_sidebar:
            self.on_toggle_sidebar(False)
        self.current_view = "home"
        self.home_page.grid(row=0, column=0, sticky="nsew")

    def show_reference_page(self):
        self._hide_all_pages()
        if self.on_toggle_sidebar:
            self.on_toggle_sidebar(True)
        self.current_view = "reference"
        self.reference_page.grid(row=0, column=0, sticky="nsew")
        self._render_reference_page()
        self.on_request_log("Consultation des fiches techniques des hacks.")

    def show_hack_menu_page(self):
        self._hide_all_pages()
        if self.on_toggle_sidebar:
            self.on_toggle_sidebar(True)
        self.current_view = "hack_menu"
        self.hack_menu_page.grid(row=0, column=0, sticky="nsew")
        self._render_hack_menu_categories()
        self._select_hack_menu_target(None)
        self.on_request_log("Ouverture du menu de hacks.")

    def show_store_page(self):
        self._hide_all_pages()
        if self.on_toggle_sidebar:
            self.on_toggle_sidebar(True)
        self.current_view = "store"
        self.store_page.grid(row=0, column=0, sticky="nsew")
        self._render_store_items()
        self.on_request_log("Ouverture du store d'équipement.")

    def show_inventory_page(self):
        self._hide_all_pages()
        if self.on_toggle_sidebar:
            self.on_toggle_sidebar(True)
        self.current_view = "inventory"
        self.inventory_page.grid(row=0, column=0, sticky="nsew")
        self._render_inventory_items()
        self.on_request_log("Consultation de l'inventaire.")

    def show_checklist_page(self):
        self._hide_all_pages()
        if self.on_toggle_sidebar:
            self.on_toggle_sidebar(True)
        self.current_view = "checklist"
        self.checklist_page.grid(row=0, column=0, sticky="nsew")
        self._render_checklist_page()
        self.on_request_log("Ouverture de la checklist de mission.")

    def show_hack_page(self):
        self._hide_all_pages()
        if self.on_toggle_sidebar:
            self.on_toggle_sidebar(True)
        self.current_view = "hack"
        self.hack_page_frame.grid(row=0, column=0, sticky="nsew")

    def _render_reference_page(self):
        for widget in self.reference_content.winfo_children():
            widget.destroy()

        for category in CATEGORIES:
            category_label = ctk.CTkLabel(
                self.reference_content,
                text=category["label"],
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#66fcf1",
            )
            category_label.grid(sticky="w", padx=16, pady=(16, 8))

            for target in category["targets"]:
                card = ctk.CTkFrame(self.reference_content, fg_color="#131820", corner_radius=12)
                card.grid(sticky="ew", padx=16, pady=(0, 12))
                card.columnconfigure(0, weight=1)

                name_label = ctk.CTkLabel(card, text=target["name"], font=ctk.CTkFont(size=16, weight="bold"), text_color="#c5c6c7")
                name_label.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4))

                info_text = (
                    f"Distance : {target['distance_label']}   Risque : {target['risk']}/5   Durée : {target.get('duration', 'N/A')}s\n"
                    f"Outils : {', '.join(target['tools'])}\n"
                    f"Description RP : {target.get('rp_description', 'Aucune description')}\n"
                    f"Mini-jeu : {target.get('minigame_title', 'Non défini')}\n"
                    f"Instruction : {target.get('minigame_instruction', 'Non définie')}\n"
                    f"Indice d'interaction : {target.get('minigame_interaction_hint', 'Non défini')}\n"
                    f"Indice : {target.get('hint', 'Aucun indice')}"
                )
                if target.get("command_examples"):
                    info_text += "\nCommandes spécifiques :\n  " + "\n  ".join(target["command_examples"])
                if target.get("sql_command"):
                    info_text += f"\nCommande SQL : {target['sql_command']}"

                details_label = ctk.CTkLabel(card, text=info_text, wraplength=760, justify="left", text_color="#c5c6c7")
                details_label.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 12))

    def _render_hack_menu_categories(self):
        for widget in self.hack_menu_list.winfo_children():
            widget.destroy()

        for category in CATEGORIES:
            category_label = ctk.CTkLabel(
                self.hack_menu_list,
                text=category["label"],
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#66fcf1",
            )
            category_label.grid(sticky="w", padx=16, pady=(16, 8))

            for target in category["targets"]:
                button = ctk.CTkButton(
                    self.hack_menu_list,
                    text=target["name"],
                    command=lambda t=target: self._select_hack_menu_target(t),
                    fg_color="#1f2833",
                    hover_color="#0b5f5f",
                    anchor="w",
                )
                button.grid(sticky="ew", padx=16, pady=4)

    def _select_hack_menu_target(self, target):
        self.selected_hack_menu_target = target
        if not target:
            self.hack_menu_title.configure(text="Sélectionnez un hack pour voir sa fiche.")
            self.hack_menu_details.configure(text="")
            self.hack_menu_launch_button.configure(state="disabled")
            return

        self.hack_menu_title.configure(text=target["name"])
        details = (
            f"Distance : {target['distance_label']}\n"
            f"Risque : {target['risk']}/5\n"
            f"Durée : {target.get('duration', 'N/A')}s\n"
            f"Outils : {', '.join(target['tools'])}\n"
            f"Description RP : {target.get('rp_description', 'Aucune description')}\n"
            f"Instruction : {target.get('minigame_instruction', 'Non définie')}\n"
            f"Indice : {target.get('minigame_interaction_hint', 'Non défini')}\n"
            f"Indice : {target.get('hint', 'Aucun indice')}"
        )
        if target.get("command_examples"):
            details += "\nCommandes spécifiques :\n  " + "\n  ".join(target["command_examples"])
        if target.get("sql_command"):
            details += f"\nCommande SQL : {target['sql_command']}"
        self.hack_menu_details.configure(text=details)
        self.hack_menu_launch_button.configure(state="normal")

    def _launch_selected_hack(self):
        if not self.selected_hack_menu_target:
            return
        self.show_hack_page()
        self.start_hack(self.selected_hack_menu_target, self.current_profile)

    def _render_store_items(self):
        for widget in self.store_list.winfo_children():
            widget.destroy()

        filtered_items = self._get_filtered_store_items()
        if not filtered_items:
            empty_label = ctk.CTkLabel(
                self.store_list,
                text="Aucun équipement ne correspond à la recherche.",
                wraplength=720,
                justify="center",
                text_color="#b0bcc5",
            )
            empty_label.grid(sticky="n", padx=16, pady=24)
            return

        for item in filtered_items:
            owned = item["id"] in self.inventory
            label_text = f"{item['name']} — {item['price']} $"
            if owned:
                label_text += " (acheté)"

            button = ctk.CTkButton(
                self.store_list,
                text=label_text,
                command=lambda i=item: self._select_store_item(i),
                fg_color="#1f2833" if not owned else "#2f3a43",
                hover_color="#0b5f5f",
                anchor="w",
            )
            button.grid(sticky="ew", padx=16, pady=6)

    def _get_filtered_store_items(self):
        query = self.store_search_var.get().strip().lower()
        items = sorted(STORE_ITEMS, key=lambda item: item["price"])
        if not query:
            return items

        filtered = []
        for item in items:
            haystack = " ".join(
                [item["name"], item["category"], item["description"], item["details"]]
            ).lower()
            if query in haystack:
                filtered.append(item)
        return filtered

    def _clear_store_search(self):
        self.store_search_var.set("")
        self._render_store_items()

    def _remove_inventory_item(self, item_id):
        if item_id not in self.inventory:
            return
        self.inventory.remove(item_id)
        self.inventory_status_label.configure(text="Objet supprimé de l'inventaire.")
        self.on_request_log(f"Objet retiré de l'inventaire : {item_id}")
        self._render_inventory_items()
        if self.current_view == "store":
            self._render_store_items()

    def _render_checklist_page(self):
        for widget in self.checklist_frame.winfo_children():
            widget.destroy()

        self.checklist_vars.clear()
        for category in CATEGORIES:
            cat_label = ctk.CTkLabel(
                self.checklist_frame,
                text=category["label"],
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#7dc4e4",
            )
            cat_label.grid(sticky="w", padx=16, pady=(16, 8))

            for target in category["targets"]:
                var = ctk.BooleanVar(value=False)
                self.checklist_vars[target["id"]] = (var, target)
                checkbox = ctk.CTkCheckBox(
                    self.checklist_frame,
                    text=target["name"],
                    variable=var,
                    command=self._update_checklist_summary,
                    text_color="#b0bcc5",
                    hover_color="#0b5f5f",
                    fg_color="#1f2833",
                )
                checkbox.grid(sticky="ew", padx=16, pady=4)

        self._update_checklist_summary()

    def _update_checklist_summary(self):
        selected = [target for var, target in self.checklist_vars.values() if var.get()]
        if not selected:
            self.checklist_summary.configure(text="Sélectionnez un ou plusieurs hacks pour afficher les outils requis.")
            return

        tools = sorted({tool for target in selected for tool in target["tools"]})
        selected_names = ", ".join(target["name"] for target in selected)
        summary = (
            f"Hacks sélectionnés : {selected_names}\n"
            f"Outils requis : {', '.join(tools)}"
        )
        self.checklist_summary.configure(text=summary)

    def _select_store_item(self, item):
        self.selected_store_item = item
        self.store_item_name.configure(text=item["name"])
        self.store_item_description.configure(text=item["description"])
        self.store_item_details.configure(text=item["details"])
        self.store_item_price.configure(text=f"Prix : {item['price']} $")
        self.store_purchase_status.configure(text="")
        self._update_store_action()

    def _update_store_action(self):
        if not self.selected_store_item:
            self.store_buy_button.configure(state="disabled")
            return
        if self.selected_store_item["id"] in self.inventory:
            self.store_buy_button.configure(state="disabled", text="Déjà acheté")
        else:
            self.store_buy_button.configure(state="normal", text="Acheter")

    def _purchase_selected_item(self):
        if not self.selected_store_item:
            return

        item_id = self.selected_store_item["id"]
        if item_id in self.inventory:
            self.store_purchase_status.configure(text="Cet équipement est déjà dans votre inventaire.")
            return

        self.inventory.add(item_id)
        self.store_purchase_status.configure(text=f"Achat validé : {self.selected_store_item['name']} a été ajouté à l'inventaire.")
        self.on_request_log(f"Achat effectué : {self.selected_store_item['name']}")
        self._render_store_items()
        self._update_store_action()

    def _render_inventory_items(self):
        self.inventory_status_label.configure(text="")
        for widget in self.inventory_content.winfo_children():
            widget.destroy()

        owned_items = [item for item in STORE_ITEMS if item["id"] in self.inventory]
        if not owned_items:
            empty_label = ctk.CTkLabel(
                self.inventory_content,
                text="Votre inventaire est vide. Achetez de l'équipement pour le remplir.",
                wraplength=760,
                justify="center",
                text_color="#b0bcc5",
            )
            empty_label.grid(sticky="n", padx=16, pady=24)
            return

        for item in owned_items:
            card = ctk.CTkFrame(self.inventory_content, fg_color="#131820", corner_radius=12)
            card.grid(sticky="ew", padx=16, pady=(12, 0))
            card.columnconfigure(0, weight=1)
            card.columnconfigure(1, weight=0)

            name_label = ctk.CTkLabel(card, text=item["name"], font=ctk.CTkFont(size=16, weight="bold"), text_color="#d3d7db")
            name_label.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4), columnspan=2)

            info_text = (
                f"Catégorie : {item['category']}   Prix : {item['price']} $\n"
                f"Description : {item['description']}\n"
                f"Détails : {item['details']}"
            )
            details_label = ctk.CTkLabel(card, text=info_text, wraplength=760, justify="left", text_color="#b0bcc5")
            details_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=12, pady=(0, 12))

            remove_button = ctk.CTkButton(
                card,
                text="Retirer",
                command=lambda item_id=item["id"]: self._remove_inventory_item(item_id),
                fg_color="#ff5555",
            )
            remove_button.grid(row=2, column=1, sticky="e", padx=12, pady=(0, 12))

        self.inventory_status_label.configure(text="Cliquez sur Retirer pour supprimer un équipement de l'inventaire.")

    def show_placeholder(self):
        self.show_home_page()

    def show_target(self, target):
        self.current_target = target
        self.show_hack_page()
        self.failure_banner.grid_remove()
        self.target_name.configure(text=target["name"])
        self.distance_label.configure(text=target["distance_label"])
        self.risk_label.configure(text=f"Niveau de risque : {target['risk']}/5")
        self.alert_label.configure(text=f"Alerte probable : {self._alert_type(target)}")
        self.tools_label.configure(text="Outils requis : " + ", ".join(target["tools"]))
        self.hint_label.configure(text=f"Indice : {target['hint']}")
        self.status_label.configure(text="Statut : Prêt")

    def show_briefing(self):
        if self.current_target is None:
            self.status_label.configure(text="Statut : Sélectionnez d'abord une cible.")
            return
        BriefingDialog(self, self.current_target, self.current_profile, self._on_briefing_result)

    def request_start_hack(self):
        if self.current_target is None:
            self.on_request_log("Aucune cible sélectionnée. Choisissez une cible avant de démarrer.")
            self.status_label.configure(text="Statut : Choisissez une cible.")
            return
        self.on_start_hack(self.current_target)

    def start_hack(self, target, profile_name):
        self.current_target = target
        self.current_profile = profile_name
        self._reset_view()
        self.failure_banner.grid_remove()
        self.target_name.configure(text=target["name"])
        self.distance_label.configure(text=target["distance_label"])
        self.alert_label.configure(text=f"Alerte probable : {self._alert_type(target)}")
        self.tools_label.configure(text="Outils requis : " + ", ".join(target["tools"]))
        self.hint_label.configure(text=f"Indice : {target['hint']}")
        self.status_label.configure(text="Statut : Initialisation du hack...")
        self._load_game(target, profile_name)

    def _load_game(self, target, profile):
        if self.active_game:
            self.active_game.destroy()

        game_class = MINI_GAME_CLASSES.get(target["interaction"], MINI_GAME_CLASSES["terminal"])
        self.active_game = HybridHackGame(self.game_area, target, manual_game_class=game_class, on_complete=self._on_game_complete, profile=profile)
        self.active_game.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        self.status_label.configure(text="Statut : Mini-jeu en cours...")

    def _on_game_complete(self, success):
        if success:
            self.status_label.configure(text="Statut : Succès ! Hack terminé.")
            self.on_request_log(f"Hack réussi : {self.current_target['name']}")
        else:
            self.status_label.configure(text="Statut : Échec du hack.")
            self._show_failure_banner(self.current_target)
            self.on_request_log(f"Hack échoué : {self.current_target['name']}")

    def _on_briefing_result(self, proceed):
        if proceed and self.current_target:
            self.start_hack(self.current_target, "Intermédiaire")

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
        if target["risk"] <= 2:
            return "Police locale"
        if target["risk"] <= 4:
            return "Police étatique"
        if target["risk"] >= 5:
            return "Police fédérale"
        return "Autre"
