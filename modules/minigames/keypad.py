import customtkinter as ctk


class KeypadCodeGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete, profile=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_complete = on_complete
        self.code = target.get("keypad_code", "7429")

        self.columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Mini-jeu : Clavier numérique", font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        instruction = ctk.CTkLabel(
            self,
            text="Entrez le code numérique correct sur le pavé pour déverrouiller le système.",
            text_color="#c5c6c7",
            wraplength=700,
            justify="left",
        )
        instruction.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))

        self.code_label = ctk.CTkLabel(self, text=f"Code ciblé : {self.code}", text_color="#8be9fd", wraplength=700, justify="left")
        self.code_label.grid(row=2, column=0, sticky="w", padx=12, pady=(0, 12))

        self.code_entry = ctk.CTkEntry(self, placeholder_text="0000", fg_color="#0b0c10", text_color="#c5c6c7")
        self.code_entry.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.code_entry.bind("<Return>", lambda event: self._submit())

        self.submit_button = ctk.CTkButton(self, text="Valider", command=self._submit, fg_color="#45a29e")
        self.submit_button.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 12))

        self.feedback = ctk.CTkLabel(self, text="", text_color="#8be9fd")
        self.feedback.grid(row=5, column=0, sticky="w", padx=16, pady=(0, 12))

    def _submit(self):
        value = self.code_entry.get().strip()
        if value == self.code:
            self.feedback.configure(text="Code correct. Accès débloqué.")
            self.after(700, lambda: self.on_complete(True))
        else:
            self.feedback.configure(text="Code incorrect. Réessayez.")
