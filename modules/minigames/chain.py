import customtkinter as ctk


class ChainGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete, profile=None, custom_title=None, custom_instruction=None, custom_hint=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_complete = on_complete
        self.steps = ["Phase 1 : Reconnaissance", "Phase 2 : Exploitation", "Phase 3 : Pivot", "Phase 4 : Extraction"]
        self.current_step = 0

        self.columnconfigure(0, weight=1)

        title_text = custom_title or "Mini-jeu : Chaîne d'exploits"
        title = ctk.CTkLabel(self, text=title_text, font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        instruction_text = custom_instruction or "Complétez chaque étape de la chaîne pour progresser vers l'accès final."
        self.instruction_label = ctk.CTkLabel(self, text=instruction_text, text_color="#c5c6c7", wraplength=700, justify="left")
        self.instruction_label.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))

        self.step_label = ctk.CTkLabel(self, text=self.steps[self.current_step], text_color="#c5c6c7", wraplength=700, justify="left")
        self.step_label.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 8))

        hint_text = custom_hint or "Interaction attendue : passez à chaque étape jusqu'à ce que la chaîne soit complète."
        self.hint_label = ctk.CTkLabel(self, text=hint_text, text_color="#8be9fd", wraplength=700, justify="left")
        self.hint_label.grid(row=3, column=0, sticky="w", padx=16, pady=(0, 8))

        self.next_button = ctk.CTkButton(self, text="Suivant", command=self._advance, fg_color="#45a29e")
        self.next_button.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 12))

        self.feedback_label = ctk.CTkLabel(self, text="Complétez chaque étape en chainant les actions.", text_color="#8be9fd")
        self.feedback_label.grid(row=5, column=0, sticky="w", padx=16, pady=(0, 12))

    def _advance(self):
        self.current_step += 1
        if self.current_step >= len(self.steps):
            self.feedback_label.configure(text="Succès : chaîne d'exploits terminée.")
            self.after(800, lambda: self.on_complete(True))
            self.next_button.configure(state="disabled")
            return
        self.step_label.configure(text=self.steps[self.current_step])
        self.feedback_label.configure(text=f"Étape suivante : {self.steps[self.current_step]}")
