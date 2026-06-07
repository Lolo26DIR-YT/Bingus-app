import random
import customtkinter as ctk


class SequenceGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete, profile=None, custom_title=None, custom_instruction=None, custom_hint=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_complete = on_complete
        self.sequence = self._build_sequence()
        self.current_index = 0

        self.columnconfigure(0, weight=1)

        title_text = custom_title or "Mini-jeu : Séquence de boutons"
        title = ctk.CTkLabel(self, text=title_text, font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        instruction_text = custom_instruction or f"Répliquez la séquence suivante : {' '.join(self.sequence)}"
        instructions = ctk.CTkLabel(self, text=instruction_text, text_color="#c5c6c7", wraplength=700, justify="left")
        instructions.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))

        hint_text = custom_hint or "Interaction attendue : reproduire la séquence avec les boutons disponibles."
        self.hint_label = ctk.CTkLabel(self, text=hint_text, text_color="#8be9fd", wraplength=700, justify="left")
        self.hint_label.grid(row=2, column=0, sticky="w", padx=12, pady=(0, 8))

        self.button_frame = ctk.CTkFrame(self, fg_color="#0b0c10")
        self.button_frame.grid(row=3, column=0, sticky="ew", padx=12, pady=12)
        self.button_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.status_label = ctk.CTkLabel(self, text="Séquence à reproduire...", text_color="#c5c6c7")
        self.status_label.grid(row=4, column=0, sticky="w", padx=12, pady=(0, 12))

        for index, key in enumerate(["A", "B", "X", "Y"]):
            ctk.CTkButton(
                self.button_frame,
                text=key,
                command=lambda value=key: self._press(value),
                fg_color="#1f2833",
                hover_color="#0b5f5f",
            ).grid(row=0, column=index, sticky="ew", padx=8, pady=8)

        self.result_label = ctk.CTkLabel(self, text="", text_color="#8be9fd")
        self.result_label.grid(row=4, column=0, sticky="w", padx=12, pady=(0, 12))

    def _build_sequence(self):
        options = ["A", "B", "X", "Y"]
        return [random.choice(options) for _ in range(5)]

    def _press(self, value):
        expected = self.sequence[self.current_index]
        if value == expected:
            self.current_index += 1
            self.status_label.configure(text=f"Correct ({self.current_index}/{len(self.sequence)})")
            if self.current_index >= len(self.sequence):
                self.result_label.configure(text="Succès : séquence complétée !")
                self.after(700, lambda: self.on_complete(True))
        else:
            self.result_label.configure(text="Erreur : séquence incorrecte. Recommencez.")
            self.current_index = 0
