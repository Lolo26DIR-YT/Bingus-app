import random
import customtkinter as ctk


class ThermalScanGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete, profile=None, custom_title=None, custom_instruction=None, custom_hint=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_complete = on_complete
        self.heat_values = [random.randint(20, 99) for _ in range(6)]
        self.correct_order = sorted(self.heat_values, reverse=True)
        self.selected = []

        self.columnconfigure(0, weight=1)

        title_text = custom_title or "Mini-jeu : Thermique"
        title = ctk.CTkLabel(self, text=title_text, font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        instruction = ctk.CTkLabel(self, text=custom_instruction or "Cliquez sur les touches dans l'ordre décroissant de chaleur.", text_color="#c5c6c7", wraplength=700, justify="left")
        instruction.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))

        hint_text = custom_hint or "Interaction attendue : cliquez sur les zones dans l'ordre de température."
        self.hint_label = ctk.CTkLabel(self, text=hint_text, text_color="#8be9fd", wraplength=700, justify="left")
        self.hint_label.grid(row=2, column=0, sticky="w", padx=12, pady=(0, 8))

        self.button_frame = ctk.CTkFrame(self, fg_color="#0b0c10")
        self.button_frame.grid(row=2, column=0, sticky="ew", padx=16, pady=12)
        self.button_frame.columnconfigure(tuple(range(6)), weight=1)

        random.shuffle(self.heat_values)
        for index, value in enumerate(self.heat_values):
            ctk.CTkButton(
                self.button_frame,
                text=f"{value}°",
                command=lambda val=value: self._press(val),
                fg_color="#1f2833",
            ).grid(row=0, column=index, sticky="ew", padx=6, pady=8)

        self.feedback_label = ctk.CTkLabel(self, text="Ordre à suivre : décroissant.", text_color="#8be9fd")
        self.feedback_label.grid(row=3, column=0, sticky="w", padx=16, pady=(0, 12))

    def _press(self, value):
        self.selected.append(value)
        if self.selected != self.correct_order[: len(self.selected)]:
            self.feedback_label.configure(text="Erreur thermique. Recommencez.")
            self.selected = []
            return
        if len(self.selected) == len(self.correct_order):
            self.feedback_label.configure(text="Succès thermique !")
            self.after(600, lambda: self.on_complete(True))
