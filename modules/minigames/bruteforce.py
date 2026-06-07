import random
import customtkinter as ctk


class BruteForceGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete, profile=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_complete = on_complete
        self.progress = 0
        self.interference = random.randint(8, 18)

        self.columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Mini-jeu : Brute-force simulé", font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(self, text="Attente du prochain cycle...", text_color="#c5c6c7")
        self.status_label.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 12))

        self.start_button = ctk.CTkButton(self, text="Démarrer le bruteforce", command=self._tick, fg_color="#45a29e")
        self.start_button.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 12))

    def _tick(self):
        self.start_button.configure(state="disabled")
        self._advance()

    def _advance(self):
        self.progress += random.uniform(0.08, 0.2)
        self.progress_bar.set(min(1.0, self.progress))
        if self.progress >= 1.0:
            self.status_label.configure(text="Bruteforce terminé, accès accordé.")
            self.after(800, lambda: self.on_complete(True))
            return

        if random.random() < 0.18:
            self.status_label.configure(text="Interférence détectée. Ajustement du cycle...")
        else:
            self.status_label.configure(text="Cycle en cours...")

        self.after(self.interference * 20, self._advance)
