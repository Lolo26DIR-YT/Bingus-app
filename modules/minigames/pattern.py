import customtkinter as ctk


class PatternMatchGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete, profile=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_complete = on_complete
        self.sequence = target.get("pattern_sequence", [1, 3, 4, 2])
        self.attempt = []

        self.columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Mini-jeu : Correspondance de motif", font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        description = ctk.CTkLabel(
            self,
            text="Reproduisez la bonne séquence de boutons pour contourner le système.",
            text_color="#c5c6c7",
            wraplength=700,
            justify="left",
        )
        description.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))

        self.sequence_label = ctk.CTkLabel(self, text=f"Pattern à reproduire : {self.sequence}", text_color="#8be9fd", wraplength=700, justify="left")
        self.sequence_label.grid(row=2, column=0, sticky="w", padx=12, pady=(0, 12))

        buttons_frame = ctk.CTkFrame(self, fg_color="#0b0f16")
        buttons_frame.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 12))
        buttons_frame.columnconfigure(tuple(range(6)), weight=1)

        for i in range(1, 7):
            button = ctk.CTkButton(
                buttons_frame,
                text=str(i),
                command=lambda value=i: self._press(value),
                fg_color="#1f2833",
                hover_color="#0b5f5f",
            )
            button.grid(row=0, column=i - 1, sticky="ew", padx=4, pady=4)

        self.status_label = ctk.CTkLabel(self, text="", text_color="#f1fa8c", wraplength=700, justify="left")
        self.status_label.grid(row=4, column=0, sticky="w", padx=12, pady=(0, 12))

        self.reset_button = ctk.CTkButton(self, text="Réinitialiser", command=self._reset, fg_color="#45a29e")
        self.reset_button.grid(row=5, column=0, sticky="ew", padx=12, pady=(0, 12))

    def _press(self, value):
        self.attempt.append(value)
        if len(self.attempt) < len(self.sequence):
            self.status_label.configure(text=f"Séquence partielle : {'-'.join(str(x) for x in self.attempt)}")
            return

        if self.attempt == self.sequence:
            self.status_label.configure(text="Séquence correcte. Accès autorisé.")
            self.after(700, lambda: self.on_complete(True))
        else:
            self.status_label.configure(text="Séquence incorrecte. Réessayez.")
            self.after(800, self._reset)

    def _reset(self):
        self.attempt = []
        self.status_label.configure(text="")
