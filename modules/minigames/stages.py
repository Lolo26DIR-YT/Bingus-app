import customtkinter as ctk


class StageProgressGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete, profile=None, custom_title=None, custom_instruction=None, custom_hint=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_complete = on_complete
        self.stages = [
            "Phase 1 : Infiltration du réseau",
            "Phase 2 : Établissement du relais",
            "Phase 3 : Contournement du firewall",
            "Phase 4 : Extraction des données",
            "Phase 5 : Effacement des traces",
        ]
        self.index = 0

        self.columnconfigure(0, weight=1)

        title_text = custom_title or "Mini-jeu : Progression par étapes"
        title = ctk.CTkLabel(self, text=title_text, font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        self.instruction_label = ctk.CTkLabel(self, text=custom_instruction or "Progression par étapes pour finaliser le hack.", text_color="#c5c6c7", wraplength=700, justify="left")
        self.instruction_label.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))

        self.stage_label = ctk.CTkLabel(self, text=self.stages[self.index], text_color="#c5c6c7", wraplength=700, justify="left")
        self.stage_label.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 8))

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.progress_bar.set(0.0)

        hint_text = custom_hint or "Interaction attendue : complétez chaque étape jusqu'à la fin."
        self.hint_label = ctk.CTkLabel(self, text=hint_text, text_color="#8be9fd", wraplength=700, justify="left")
        self.hint_label.grid(row=4, column=0, sticky="w", padx=16, pady=(0, 8))

        self.next_button = ctk.CTkButton(self, text="Compléter l'étape", command=self._next_stage, fg_color="#45a29e")
        self.next_button.grid(row=5, column=0, sticky="ew", padx=16, pady=(0, 12))

    def _next_stage(self):
        self.index += 1
        self.progress_bar.set(self.index / len(self.stages))
        if self.index >= len(self.stages):
            self.stage_label.configure(text="Toutes les étapes sont terminées.")
            self.next_button.configure(state="disabled")
            self.after(800, lambda: self.on_complete(True))
            return
        self.stage_label.configure(text=self.stages[self.index])
