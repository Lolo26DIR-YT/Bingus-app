import customtkinter as ctk
from modules.ui.briefing import BriefingDialog
from modules.utils.profile import OperatorProfile
from modules.utils.risk_engine import RiskEngine
from modules.minigames.sequence import SequenceGame
from modules.minigames.wiring import WiringGame
from modules.minigames.frequency import FrequencySweepGame
from modules.minigames.terminal import TerminalCommandGame
from modules.minigames.bruteforce import BruteForceGame
from modules.minigames.chain import ChainGame
from modules.minigames.radio import RadioDecryptGame
from modules.minigames.thermal import ThermalScanGame
from modules.minigames.stages import StageProgressGame

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
}


class MainPanel(ctk.CTkFrame):
    def __init__(self, parent, on_start_hack, on_request_log, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_start_hack = on_start_hack
        self.on_request_log = on_request_log
        self.current_target = None
        self.current_profile = "Intermédiaire"
        self.active_game = None
        self.risk_engine = None
        self.risk_job = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)

        self.title_label = ctk.CTkLabel(self, text="Bingus Hack Simulator", font=ctk.CTkFont(size=22, weight="bold"), text_color="#66fcf1")
        self.title_label.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        self.summary_frame = ctk.CTkFrame(self, fg_color="#0b0f16")
        self.summary_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.summary_frame.columnconfigure((0, 1), weight=1)

        self.target_name = ctk.CTkLabel(self.summary_frame, text="Aucune cible sélectionnée.", font=ctk.CTkFont(size=18, weight="bold"), text_color="#c5c6c7")
        self.target_name.grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=12)

        self.distance_label = ctk.CTkLabel(self.summary_frame, text="", text_color="#66fcf1")
        self.distance_label.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))
        self.risk_label = ctk.CTkLabel(self.summary_frame, text="", text_color="#ffb86c")
        self.risk_label.grid(row=1, column=1, sticky="e", padx=16, pady=(0, 8))

        self.tools_label = ctk.CTkLabel(self.summary_frame, text="", wraplength=720, justify="left", text_color="#c5c6c7")
        self.tools_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 12))

        self.hint_label = ctk.CTkLabel(self.summary_frame, text="", wraplength=720, justify="left", text_color="#8be9fd")
        self.hint_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 16))

        self.button_frame = ctk.CTkFrame(self, fg_color="#0b0f16")
        self.button_frame.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.button_frame.columnconfigure((0, 1), weight=1)

        self.brief_button = ctk.CTkButton(self.button_frame, text="Briefing", command=self.show_briefing, fg_color="#1f2833")
        self.brief_button.grid(row=0, column=0, sticky="ew", padx=(16, 8), pady=12)
        self.start_button = ctk.CTkButton(self.button_frame, text="Lancer le hack", command=self.request_start_hack, fg_color="#45a29e")
        self.start_button.grid(row=0, column=1, sticky="ew", padx=(8, 16), pady=12)

        self.progress_frame = ctk.CTkFrame(self, fg_color="#0b0f16")
        self.progress_frame.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.progress_frame.columnconfigure((0, 1), weight=1)

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=12)
        self.progress_bar.set(0.0)

        self.risk_value = ctk.CTkLabel(self.progress_frame, text="Risque : 0%", text_color="#ff5555")
        self.risk_value.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 12))
        self.status_label = ctk.CTkLabel(self.progress_frame, text="Statut : En attente", text_color="#c5c6c7")
        self.status_label.grid(row=1, column=1, sticky="e", padx=16, pady=(0, 12))

        self.game_area = ctk.CTkFrame(self, fg_color="#0b0f16")
        self.game_area.grid(row=4, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.game_area.columnconfigure(0, weight=1)
        self.game_area.rowconfigure(0, weight=1)

    def show_placeholder(self):
        self._reset_view()
        self.target_name.configure(text="Sélectionnez une cible à pirater")
        self.tools_label.configure(text="")
        self.distance_label.configure(text="")
        self.risk_label.configure(text="")
        self.status_label.configure(text="Statut : En attente")

    def show_target(self, target):
        self._reset_view()
        self.current_target = target
        self.target_name.configure(text=target["name"])
        self.distance_label.configure(text=target["distance_label"])
        self.risk_label.configure(text=f"Niveau de risque : {target['risk']}/5")
        self.tools_label.configure(text="Outils requis : " + ", ".join(target["tools"]))
        self.hint_label.configure(text=f"Indice : {target['hint']}")
        self.progress_bar.set(0.0)
        self.risk_value.configure(text="Risque : 0%")
        self.status_label.configure(text="Statut : Prêt")

    def show_briefing(self):
        if self.current_target is None:
            self.status_label.configure(text="Statut : Sélectionnez d'abord une cible.")
            return
        BriefingDialog(self, self.current_target, self.current_profile, self._on_briefing_result)

    def request_start_hack(self):
        if self.current_target is None:
            self.on_request_log("Aucune cible sélectionnée. Choisissez une cible avant de démarrer.")
            self.status_label.configure(text="Statut : Choisissez une cible.")
            return
        self.on_start_hack(self.current_target)

    def start_hack(self, target, profile_name):
        self.current_target = target
        self.current_profile = profile_name
        self._reset_view()
        self.target_name.configure(text=target["name"])
        self.distance_label.configure(text=target["distance_label"])
        self.tools_label.configure(text="Outils requis : " + ", ".join(target["tools"]))
        self.hint_label.configure(text=f"Indice : {target['hint']}")
        self.status_label.configure(text="Statut : Initialisation du hack...")

        profile = OperatorProfile(profile_name)
        self.risk_engine = RiskEngine(base_risk=target["risk"], profile=profile)
        self.risk_engine.start()
        self._start_risk_loop()
        self._load_game(target, profile)

    def _load_game(self, target, profile):
        if self.active_game:
            self.active_game.destroy()

        game_class = MINI_GAME_CLASSES.get(target["interaction"], TerminalCommandGame)
        self.active_game = game_class(self.game_area, target, on_complete=self._on_game_complete, profile=profile)
        self.active_game.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        self.status_label.configure(text="Statut : Mini-jeu en cours...")

    def _on_game_complete(self, success):
        self._stop_risk_loop()
        if success:
            self.progress_bar.set(1.0)
            self.status_label.configure(text="Statut : Succès ! Hack terminé.")
            self.on_request_log(f"Hack réussi : {self.current_target['name']}")
        else:
            self.progress_bar.set(0.0)
            self.status_label.configure(text="Statut : Échec du hack.")
            self.on_request_log(f"Hack échoué : {self.current_target['name']}")

    def _on_briefing_result(self, proceed):
        if proceed and self.current_target:
            self.start_hack(self.current_target, "Intermédiaire")

    def _start_risk_loop(self):
        self._update_risk_meter()

    def _update_risk_meter(self):
        if self.risk_engine is None:
            return
        risk_value = self.risk_engine.next_tick()
        self.risk_value.configure(text=f"Risque : {risk_value}%")
        self.progress_bar.set(min(1.0, risk_value / 100.0))
        if risk_value >= 100:
            self._stop_risk_loop()
            self._on_game_complete(False)
            return
        self.risk_job = self.after(2500, self._update_risk_meter)

    def _stop_risk_loop(self):
        if self.risk_job:
            self.after_cancel(self.risk_job)
            self.risk_job = None

    def _reset_view(self):
        if self.active_game:
            self.active_game.destroy()
            self.active_game = None
        self._stop_risk_loop()
        self.progress_bar.set(0.0)
