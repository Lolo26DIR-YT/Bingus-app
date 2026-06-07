import customtkinter as ctk


class StageProgressGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete, profile=None, **kwargs):
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

        title = ctk.CTkLabel(self, text="Mini-jeu : Progression par étapes", font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        self.stage_label = ctk.CTkLabel(self, text=self.stages[self.index], text_color="#c5c6c7", wraplength=700, justify="left")
        self.stage_label.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.progress_bar.set(0.0)

        self.next_button = ctk.CTkButton(self, text="Compléter l'étape", command=self._next_stage, fg_color="#45a29e")
        self.next_button.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 12))

    def _next_stage(self):
        self.index += 1
        self.progress_bar.set(self.index / len(self.stages))
        if self.index >= len(self.stages):
            self.stage_label.configure(text="Toutes les étapes sont terminées.")
            self.next_button.configure(state="disabled")
            self.after(800, lambda: self.on_complete(True))
            return
        self.stage_label.configure(text=self.stages[self.index])
