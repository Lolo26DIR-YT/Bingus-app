import customtkinter as ctk


class RadioDecryptGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete, profile=None, custom_title=None, custom_instruction=None, custom_hint=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_complete = on_complete
        self.fragments = ["SND", "GAR", "AIV", "TEU"]
        self.ordered = []

        self.columnconfigure(0, weight=1)

        title_text = custom_title or "Mini-jeu : Déchiffrement radio"
        title = ctk.CTkLabel(self, text=title_text, font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        instruction_text = custom_instruction or "Assemblez les fragments dans le bon ordre."
        instruction = ctk.CTkLabel(self, text=instruction_text, text_color="#c5c6c7", wraplength=700, justify="left")
        instruction.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))

        hint_text = custom_hint or "Interaction attendue : sélectionnez les fragments pour former le message correct."
        self.hint_label = ctk.CTkLabel(self, text=hint_text, text_color="#8be9fd", wraplength=700, justify="left")
        self.hint_label.grid(row=2, column=0, sticky="w", padx=12, pady=(0, 8))

        self.fragment_frame = ctk.CTkFrame(self, fg_color="#0b0c10")
        self.fragment_frame.grid(row=3, column=0, sticky="ew", padx=16, pady=12)
        self.fragment_frame.columnconfigure((0, 1, 2, 3), weight=1)

        for index, token in enumerate(self.fragments):
            ctk.CTkButton(
                self.fragment_frame,
                text=token,
                command=lambda value=token: self._select_fragment(value),
                fg_color="#1f2833",
            ).grid(row=0, column=index, sticky="ew", padx=6, pady=8)

        self.sequence_label = ctk.CTkLabel(self, text="Séquence actuelle : ", text_color="#c5c6c7")
        self.sequence_label.grid(row=3, column=0, sticky="w", padx=16, pady=(0, 12))

        self.clear_button = ctk.CTkButton(self, text="Effacer", command=self._clear, fg_color="#ff5555")
        self.clear_button.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 12))

    def _select_fragment(self, fragment):
        if fragment in self.ordered:
            return
        self.ordered.append(fragment)
        self.sequence_label.configure(text="Séquence actuelle : " + "-".join(self.ordered))
        if len(self.ordered) == len(self.fragments):
            if self.ordered == ["SND", "GAR", "AIV", "TEU"]:
                self.after(500, lambda: self.on_complete(True))
            else:
                self._clear()

    def _clear(self):
        self.ordered = []
        self.sequence_label.configure(text="Séquence actuelle : ")
