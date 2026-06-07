import customtkinter as ctk
from modules.minigames.core import create_minigame


class ManualHackDialog(ctk.CTkToplevel):
    def __init__(self, parent, target, manual_game_class, on_complete, profile=None):
        super().__init__(parent)
        self.title("Phase manuelle requise")
        self.geometry("760x620")
        self.configure(fg_color="#131820")
        self.manual_game_class = manual_game_class
        self.on_complete = on_complete
        self.profile = profile
        self.target = target
        self.success = False

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        header = ctk.CTkLabel(self, text="Phase manuelle du hack", font=ctk.CTkFont(size=20, weight="bold"), text_color="#66fcf1")
        header.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        info = ctk.CTkLabel(
            self,
            text="Effectuez les actions demandées puis cliquez sur le bouton Fait pour que la barre de chargement puisse continuer.",
            text_color="#c5c6c7",
            wraplength=720,
            justify="left",
        )
        info.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 12))

        self.manual_frame = ctk.CTkFrame(self, fg_color="#0b0f16")
        self.manual_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 16))
        self.manual_frame.columnconfigure(0, weight=1)
        self.manual_frame.rowconfigure(1, weight=1)

        self.manual_label = ctk.CTkLabel(
            self.manual_frame,
            text=self._build_instructions(),
            text_color="#c5c6c7",
            wraplength=720,
            justify="left",
        )
        self.manual_label.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 12))

        self.interaction_hint_label = ctk.CTkLabel(
            self.manual_frame,
            text=self._build_interaction_hint(),
            text_color="#8be9fd",
            wraplength=720,
            justify="left",
        )
        self.interaction_hint_label.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 12))

        self.game_container = ctk.CTkFrame(self.manual_frame, fg_color="#131820")
        self.game_container.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.game_container.columnconfigure(0, weight=1)
        self.game_container.rowconfigure(0, weight=1)

        self.manual_game = create_minigame(
            self.game_container,
            self.target,
            self.manual_game_class,
            on_complete=self._manual_game_finished,
            profile=self.profile,
        )
        self.manual_game.grid(row=0, column=0, sticky="nsew")

        self.footer_frame = ctk.CTkFrame(self, fg_color="#0b0f16")
        self.footer_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.footer_frame.columnconfigure((0, 1), weight=1)

        self.status_label = ctk.CTkLabel(self.footer_frame, text="En attente de la validation manuelle...", text_color="#f1fa8c")
        self.status_label.grid(row=0, column=0, sticky="w", padx=16, pady=12)

        self.done_button = ctk.CTkButton(self.footer_frame, text="Fait", command=self._confirm_done, fg_color="#45a29e", state="disabled")
        self.done_button.grid(row=0, column=1, sticky="ew", padx=(8, 16), pady=12)

    def _build_instructions(self):
        instruction = self.target.get("minigame_instruction")
        if instruction:
            base = f"Instructions :\n  • {instruction.replace(' • ', '\n  • ')}"
        else:
            base = f"Instructions :\n  • {self.target.get('hint', 'Suivez les étapes du hack.') }"

        command_examples = self.target.get("command_examples")
        if command_examples:
            example_lines = "\n  • ".join(command_examples)
            return f"{base}\nCommandes spécifiques :\n  • {example_lines}"

        return base

    def _build_interaction_hint(self):
        interaction_hint = self.target.get("minigame_interaction_hint")
        if interaction_hint:
            return f"Interaction attendue : {interaction_hint}"
        interaction = self.target.get("interaction", "terminal")
        default_hints = {
            "terminal": "Entrez la bonne commande texte et appuyez sur Exécuter.",
            "wiring": "Sélectionnez un fil, puis la destination correspondante.",
            "frequency": "Ajustez le curseur et lancez le scan lorsque vous êtes proche.",
            "sequence": "Repérez l'ordre et reproduisez-le avec les boutons.",
            "bruteforce": "Lancez l'attaque et surveillez la progression.",
            "chain": "Passez d'une étape à la suivante jusqu'à la fin.",
            "radio": "Assemblez tous les fragments dans l'ordre correct.",
            "thermal": "Cliquez sur les zones les plus chaudes dans l'ordre.",
            "stages": "Complétez chaque phase pour finaliser l'accès.",
        }
        return f"Interaction attendue : {default_hints.get(interaction, 'Suivez les instructions du mini-jeu.') }"

    def _manual_game_finished(self, success):
        if not success:
            self.on_complete(False)
            self.destroy()
            return

        self.success = True
        self.status_label.configure(text="Manuel validé. Cliquez sur Fait pour terminer.")
        self.done_button.configure(state="normal")

    def _confirm_done(self):
        if not self.success:
            return
        self.on_complete(True)
        self.destroy()
