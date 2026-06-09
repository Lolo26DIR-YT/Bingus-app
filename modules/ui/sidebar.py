import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, categories, on_category_selected, on_target_selected, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_category_selected = on_category_selected
        self.on_target_selected = on_target_selected
        self.categories = categories
        self.active_category = None
        self.target_buttons = []
        self.category_buttons = {}

        self.columnconfigure(0, weight=1)

        # --- TITRE CATÉGORIES ---
        header = ctk.CTkLabel(self, text="CATEGORIES", font=ctk.CTkFont(size=14, weight="bold"), text_color="#66fcf1")
        header.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        # --- FRAME CATÉGORIES ---
        self.category_frame = ctk.CTkFrame(self, fg_color="#0b0f16")
        self.category_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))
        self.category_frame.columnconfigure(0, weight=1)

        # Création des boutons pour chaque catégorie
        for index, cat in enumerate(self.categories):
            btn = ctk.CTkButton(
                self.category_frame,
                text=cat["label"], # Utilisation de 'label' ici
                command=lambda c=cat["key"]: self.select_category(c),
                fg_color="#1f2833",
                height=30
            )
            btn.grid(row=index, column=0, sticky="ew", padx=5, pady=2)
            self.category_buttons[cat["key"]] = btn

        # --- TITRE CIBLES ---
        self.target_label = ctk.CTkLabel(self, text="CIBLES", font=ctk.CTkFont(size=14, weight="bold"), text_color="#66fcf1")
        self.target_label.grid(row=2, column=0, sticky="w", padx=12, pady=(0, 6))

        # --- ZONE CIBLES (SCROLLABLE) ---
        self.target_scroll = ctk.CTkScrollableFrame(self, fg_color="#0b0f16")
        self.target_scroll.grid(row=3, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.target_scroll.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

    def select_category(self, key):
        category = next((c for c in self.categories if c["key"] == key), None)
        if not category:
            return
        self.active_category = category
        self.on_category_selected(category)
        self._render_targets(category.get("targets", []))
        
        for button_key, button in self.category_buttons.items():
            button.configure(fg_color="#45a29e" if button_key == key else "#1f2833")

    def _render_targets(self, targets):
        # Nettoyage
        for widget in self.target_scroll.winfo_children():
            widget.destroy()
        self.target_buttons.clear()

        # Création des nouveaux boutons
        for index, target in enumerate(targets):
            # --- DÉCOUPAGE INTELLIGENT DU TEXTE ---
            raw_name = target['name']
            words = raw_name.split()
            lines = []
            current_line = ""
            
            # On regroupe les mots par paquets de 12 caractères max
            for word in words:
                if len(current_line) + len(word) <= 12:
                    current_line += (word + " ")
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            lines.append(current_line.strip())
            formatted_name = "\n".join(lines)

            button = ctk.CTkButton(
                self.target_scroll,
                text=formatted_name,
                command=lambda t=target: self.on_target_selected(t),
                fg_color="#18212b",
                hover_color="#0b5f5f",
                text_color="#c5c6c7",
                anchor="center",    # Tout centré pour une cohérence parfaite
                height=80           # Hauteur augmentée pour accueillir le texte sur 2-3 lignes
            )
            button.grid(row=index, column=0, sticky="ew", padx=8, pady=4)
            self.target_buttons.append(button)