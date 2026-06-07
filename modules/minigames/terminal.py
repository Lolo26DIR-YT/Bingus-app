import customtkinter as ctk


class TerminalCommandGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete, profile=None, custom_title=None, custom_instruction=None, custom_hint=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_complete = on_complete
        command_examples = target.get("command_examples") if target else None
        self.accepted_commands = [cmd.strip().lower() for cmd in command_examples] if command_examples else ["scan network", "exploit ssh", "inject payload", "clone badge"]

        self.columnconfigure(0, weight=1)

        title_text = custom_title or "Mini-jeu : Injection de commandes"
        title = ctk.CTkLabel(self, text=title_text, font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        instruction_text = custom_instruction or "Tapez la commande correcte pour activer l'outil."
        instruction = ctk.CTkLabel(self, text=instruction_text, text_color="#c5c6c7", wraplength=700, justify="left")
        instruction.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))

        hint_text = custom_hint or "Interaction attendue : entrez un texte de commande pertinent et exécutez-le."
        self.hint_label = ctk.CTkLabel(self, text=hint_text, text_color="#8be9fd", wraplength=700, justify="left")
        self.hint_label.grid(row=2, column=0, sticky="w", padx=12, pady=(0, 8))

        example_text = "Exemples : " + "; ".join(command_examples) if command_examples else "Exemples : scan network; exploit ssh; inject payload; clone badge"
        self.example_label = ctk.CTkLabel(self, text=example_text, text_color="#8be9fd", wraplength=700, justify="left")
        self.example_label.grid(row=3, column=0, sticky="w", padx=12, pady=(0, 8))

        self.command_entry = ctk.CTkEntry(self, placeholder_text="Entrez une commande...", fg_color="#0b0c10", text_color="#c5c6c7")
        self.command_entry.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.command_entry.bind("<Return>", lambda event: self._submit())

        self.submit_button = ctk.CTkButton(self, text="Exécuter", command=self._submit, fg_color="#45a29e")
        self.submit_button.grid(row=5, column=0, sticky="ew", padx=16, pady=(0, 12))

        self.feedback = ctk.CTkLabel(self, text="", text_color="#8be9fd")
        self.feedback.grid(row=6, column=0, sticky="w", padx=16, pady=(0, 12))

    def _submit(self):
        command = self.command_entry.get().strip().lower()
        if command in self.accepted_commands:
            self.feedback.configure(text="Commande acceptée. Attaque lancée.")
            self.after(700, lambda: self.on_complete(True))
        else:
            self.feedback.configure(text="Commande invalide. Essayez une autre instruction.")
