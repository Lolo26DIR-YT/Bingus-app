import customtkinter as ctk


class MemoryRecallGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete, profile=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_complete = on_complete
        self.sequence = target.get("memory_sequence", [4, 1, 3, 2])
        self.attempt = []
        self.sequence_visible = True

        self.columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Mini-jeu : Mémoire rapide", font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        description = ctk.CTkLabel(
            self,
            text="Mémorisez la séquence affichée, puis reproduisez-la avec les boutons.",
            text_color="#c5c6c7",
            wraplength=700,
            justify="left",
        )
        description.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))

        self.sequence_label = ctk.CTkLabel(self, text=f"Séquence : {' '.join(str(x) for x in self.sequence)}", text_color="#8be9fd", wraplength=700, justify="left")
        self.sequence_label.grid(row=2, column=0, sticky="w", padx=12, pady=(0, 12))

        self.hide_button = ctk.CTkButton(self, text="Cacher la séquence", command=self._hide_sequence, fg_color="#45a29e")
        self.hide_button.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 12))

        buttons_frame = ctk.CTkFrame(self, fg_color="#0b0f16")
        buttons_frame.grid(row=4, column=0, sticky="ew", padx=12, pady=(0, 12))
        buttons_frame.columnconfigure(tuple(range(4)), weight=1)

        for i in range(1, 5):
            button = ctk.CTkButton(
                buttons_frame,
                text=str(i),
                command=lambda value=i: self._press(value),
                fg_color="#1f2833",
                hover_color="#0b5f5f",
                state="disabled",
            )
            button.grid(row=0, column=i - 1, sticky="ew", padx=4, pady=4)
            setattr(self, f"button_{i}", button)

        self.status_label = ctk.CTkLabel(self, text="", text_color="#f1fa8c", wraplength=700, justify="left")
        self.status_label.grid(row=5, column=0, sticky="w", padx=12, pady=(0, 12))

    def _hide_sequence(self):
        self.sequence_visible = False
        self.sequence_label.configure(text="Reproduisez maintenant la séquence mémorisée.")
        self.hide_button.configure(state="disabled")
        for i in range(1, 5):
            getattr(self, f"button_{i}").configure(state="normal")

    def _press(self, value):
        if self.sequence_visible:
            return
        self.attempt.append(value)
        if len(self.attempt) < len(self.sequence):
            self.status_label.configure(text=f"Entrées : {' '.join(str(x) for x in self.attempt)}")
            return

        if self.attempt == self.sequence:
            self.status_label.configure(text="Séquence correcte. Bypass mémoire réussi.")
            self.after(700, lambda: self.on_complete(True))
        else:
            self.status_label.configure(text="Séquence incorrecte. Réessayez.")
            self.after(800, self._reset)

    def _reset(self):
        self.attempt = []
        self.sequence_visible = True
        self.sequence_label.configure(text=f"Séquence : {' '.join(str(x) for x in self.sequence)}")
        self.hide_button.configure(state="normal")
        self.status_label.configure(text="")
        for i in range(1, 5):
            getattr(self, f"button_{i}").configure(state="disabled")
