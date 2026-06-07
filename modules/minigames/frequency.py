import random
import customtkinter as ctk


class FrequencySweepGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete, profile=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_complete = on_complete
        self.secret_frequency = random.randint(24, 78)

        self.columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Mini-jeu : Balayage de fréquences", font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        self.instructions = ctk.CTkLabel(self, text="Faites glisser le curseur jusqu'à la fréquence la plus stable.", text_color="#c5c6c7")
        self.instructions.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))

        self.slider = ctk.CTkSlider(self, from_=20, to=80, number_of_steps=60, command=self._update_frequency)
        self.slider.set(50)
        self.slider.grid(row=2, column=0, sticky="ew", padx=16, pady=12)

        self.frequency_label = ctk.CTkLabel(self, text="Fréquence actuelle : 50 MHz", text_color="#c5c6c7")
        self.frequency_label.grid(row=3, column=0, sticky="w", padx=16, pady=(0, 12))

        self.check_button = ctk.CTkButton(self, text="Scanner", command=self._scan, fg_color="#45a29e")
        self.check_button.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 12))

        self.result_label = ctk.CTkLabel(self, text="", text_color="#8be9fd")
        self.result_label.grid(row=5, column=0, sticky="w", padx=16, pady=(0, 12))

    def _update_frequency(self, value):
        self.current_value = int(value)
        self.frequency_label.configure(text=f"Fréquence actuelle : {self.current_value} MHz")

    def _scan(self):
        if abs(self.current_value - self.secret_frequency) <= 3:
            self.result_label.configure(text="Signal trouvé ! Fréquence stable." )
            self.after(800, lambda: self.on_complete(True))
        else:
            self.result_label.configure(text="Aucun signal. Ajustez la fréquence et réessayez.")
