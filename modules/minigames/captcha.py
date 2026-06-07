import customtkinter as ctk


class CaptchaSolveGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete, profile=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_complete = on_complete
        self.code = target.get("captcha_code", "B1N9")

        self.columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Mini-jeu : Vérification CAPTCHA", font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        instruction = ctk.CTkLabel(
            self,
            text="Recopiez le code affiché pour contourner la validation.",
            text_color="#c5c6c7",
            wraplength=700,
            justify="left",
        )
        instruction.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))

        self.code_label = ctk.CTkLabel(self, text=f"Code CAPTCHA : {self.code}", text_color="#8be9fd", wraplength=700, justify="left")
        self.code_label.grid(row=2, column=0, sticky="w", padx=12, pady=(0, 12))

        self.entry = ctk.CTkEntry(self, placeholder_text="Recopiez le code", fg_color="#0b0c10", text_color="#c5c6c7")
        self.entry.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.entry.bind("<Return>", lambda event: self._submit())

        self.submit_button = ctk.CTkButton(self, text="Soumettre", command=self._submit, fg_color="#45a29e")
        self.submit_button.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 12))

        self.feedback = ctk.CTkLabel(self, text="", text_color="#8be9fd")
        self.feedback.grid(row=5, column=0, sticky="w", padx=16, pady=(0, 12))

    def _submit(self):
        value = self.entry.get().strip()
        if value == self.code:
            self.feedback.configure(text="CAPTCHA validé. Validation réussie.")
            self.after(700, lambda: self.on_complete(True))
        else:
            self.feedback.configure(text="Code incorrect. Essayez encore.")
