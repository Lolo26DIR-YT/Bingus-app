import customtkinter as ctk
from modules.minigames.sequence import SequenceGame
from modules.minigames.wiring import WiringGame
from modules.minigames.frequency import FrequencySweepGame
from modules.minigames.terminal import TerminalCommandGame
from modules.minigames.bruteforce import BruteForceGame
from modules.minigames.chain import ChainGame
from modules.minigames.radio import RadioDecryptGame
from modules.minigames.thermal import ThermalScanGame
from modules.minigames.stages import StageProgressGame
from modules.minigames.pattern import PatternMatchGame
from modules.minigames.memory import MemoryRecallGame
from modules.minigames.keypad import KeypadCodeGame
from modules.minigames.captcha import CaptchaSolveGame
from modules.minigames.firewall import FirewallBypassGame

MINI_GAME_CLASSES = {
    "sequence": SequenceGame,
    "wiring": WiringGame,
    "frequency": FrequencySweepGame,
    "terminal": TerminalCommandGame,
    "bruteforce": BruteForceGame,
    "chain": ChainGame,
    "radio": RadioDecryptGame,
    "thermal": ThermalScanGame,
    "stages": StageProgressGame,
    "puzzle": TerminalCommandGame,
    "pattern": PatternMatchGame,
    "memory": MemoryRecallGame,
    "keypad": KeypadCodeGame,
    "captcha": CaptchaSolveGame,
    "firewall": FirewallBypassGame,
}


def _default_minigame_title(target):
    return f"Mini-jeu : {target['name']}"


def _default_minigame_instruction(target):
    if target.get("minigame_instruction"):
        return target["minigame_instruction"]
    return f"{target.get('hint', 'Suivez les instructions spécifiques au hack.') }"


def _default_interaction_hint(target):
    if target.get("minigame_interaction_hint"):
        return target["minigame_interaction_hint"]
    interaction = target.get("interaction", "terminal")
    hints = {
        "terminal": "Tapez une commande valide en vous basant sur l’objectif du hack.",
        "wiring": "Sélectionnez et reliez les bons fils selon le schéma implicite.",
        "frequency": "Cherchez le signal actif et ajustez la fréquence avec précision.",
        "sequence": "Reproduisez la séquence dans l’ordre exact.",
        "bruteforce": "Lancez le processus et laissez-le trouver la bonne clé.",
        "chain": "Complétez chaque étape de la chaîne sans erreur.",
        "radio": "Assemblez les fragments dans le bon ordre pour décrypter le message.",
        "thermal": "Cliquez sur les zones les plus chaudes dans l’ordre décroissant.",
        "stages": "Progressez étape par étape pour finaliser l’accès.",
    }
    return hints.get(interaction, "Suivez les indications du système pour compléter le hack.")


def create_minigame(parent, target, manual_game_class, on_complete, profile=None):
    return manual_game_class(
        parent,
        target,
        on_complete,
        profile=profile,
        custom_title=_default_minigame_title(target),
        custom_instruction=_default_minigame_instruction(target),
        custom_hint=_default_interaction_hint(target),
    )


class HybridHackGame(ctk.CTkFrame):
    def __init__(self, parent, target, manual_game_class, on_complete, profile=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.target = target
        self.manual_game_class = manual_game_class
        self.on_complete = on_complete
        self.profile = profile
        self.step_index = 0
        self.phase = "auto"
        self.auto_steps = [
            f"Analyse passive de {target['name']} en cours...",
            "Préparation des modules de liaison...",
            "Vérification des vecteurs d'accès...",
        ]
        self.final_steps = [
            "Finalisation du tunnel sécurisé...",
            "Élimination des traces numériques...",
        ]
        self.current_steps = self.auto_steps

        self.columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Phase automatique du hack", font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        self.info_label = ctk.CTkLabel(self, text="Lancement du hack automatique...", text_color="#c5c6c7", wraplength=760, justify="left")
        self.info_label.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))

        self.step_label = ctk.CTkLabel(self, text="Phase automatique initiale", text_color="#8be9fd")
        self.step_label.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 8))

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.progress_bar.set(0.0)

        self.manual_hint = ctk.CTkLabel(self, text="Une phase manuelle est requise. Une nouvelle fenêtre va s'ouvrir.", text_color="#f1fa8c", wraplength=760, justify="left")
        self.manual_hint.grid(row=4, column=0, sticky="w", padx=16, pady=(0, 12))
        self.manual_hint.configure(text="Phase automatique en cours...")

        self.after(600, self._advance_auto_phase)

    def _advance_auto_phase(self):
        if self.step_index >= len(self.current_steps):
            if self.phase == "auto":
                self.manual_hint.configure(text="Phase manuelle requise : ouverture de la page de hack manuel.")
                self.after(800, self._open_manual_page)
                return
            self.on_complete(True)
            return

        self.step_label.configure(text=self.current_steps[self.step_index])
        self.info_label.configure(text=f"{self.current_steps[self.step_index]}")
        self.step_index += 1
        self.progress_bar.set(self.step_index / len(self.current_steps))
        self.after(1000, self._advance_auto_phase)

    def _open_manual_page(self):
        self.manual_window = ManualHackDialog(self, self.target, self.manual_game_class, self._manual_finished, profile=self.profile)
        self.manual_window.grab_set()

    def _manual_finished(self, success):
        if not success:
            self.on_complete(False)
            return

        self.phase = "final"
        self.current_steps = self.final_steps
        self.step_index = 0
        self.step_label.configure(text="Reprise de la phase automatique finale")
        self.progress_bar.set(0.0)
        self.info_label.configure(text="La phase manuelle est terminée. Finalisation en cours...")
        self.manual_hint.configure(text="")
        self.after(800, self._advance_auto_phase)
