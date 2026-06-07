import random
import customtkinter as ctk


class WiringGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete, profile=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_complete = on_complete
        self.pairs = self._build_pairs()
        self.selected = None
        self.matched = set()

        self.columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Mini-jeu : Câblage", font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        instructions = ctk.CTkLabel(self, text="Reliez les bons fils entre eux.", text_color="#c5c6c7")
        instructions.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))

        self.grid_frame = ctk.CTkFrame(self, fg_color="#0b0c10")
        self.grid_frame.grid(row=2, column=0, sticky="ew", padx=12, pady=12)
        self.grid_frame.columnconfigure((0, 1), weight=1)

        self.left_buttons = {}
        self.right_buttons = {}

        for index, (left, right) in enumerate(self.pairs.items()):
            left_button = ctk.CTkButton(self.grid_frame, text=left, command=lambda l=left: self._select_left(l), fg_color="#1f2833")
            left_button.grid(row=index, column=0, sticky="ew", padx=12, pady=6)
            self.left_buttons[left] = left_button

            right_button = ctk.CTkButton(self.grid_frame, text=right, command=lambda r=right: self._select_right(r), fg_color="#1f2833")
            right_button.grid(row=index, column=1, sticky="ew", padx=12, pady=6)
            self.right_buttons[right] = right_button

        self.feedback_label = ctk.CTkLabel(self, text="Sélectionnez un fil à gauche puis la destination à droite.", text_color="#c5c6c7")
        self.feedback_label.grid(row=3, column=0, sticky="w", padx=12, pady=(0, 12))

    def _build_pairs(self):
        left = ["Rouge", "Bleu", "Vert", "Jaune"]
        right = ["A", "B", "C", "D"]
        random.shuffle(right)
        return dict(zip(left, right))

    def _select_left(self, left_name):
        self.selected = left_name
        self.feedback_label.configure(text=f"Fil sélectionné : {left_name}. Choisissez la destination.")

    def _select_right(self, right_name):
        if self.selected is None:
            self.feedback_label.configure(text="Sélectionnez d'abord un fil à gauche.")
            return
        correct = self.pairs[self.selected]
        if right_name == correct:
            self.feedback_label.configure(text=f"Connecté : {self.selected} → {right_name}")
            self.left_buttons[self.selected].configure(state="disabled")
            self.right_buttons[right_name].configure(state="disabled")
            self.matched.add(self.selected)
            self.selected = None
            if len(self.matched) == len(self.pairs):
                self.feedback_label.configure(text="Succès : tous les fils sont reliés !")
                self.after(700, lambda: self.on_complete(True))
        else:
            self.feedback_label.configure(text="Mauvaise connexion, reprenez depuis le début.")
            self.selected = None
