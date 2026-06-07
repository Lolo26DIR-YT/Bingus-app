#!/usr/bin/env python3
"""
Bingus Hack Panel — Panneau de contrôle RP pour sessions GTA V.
Outil visuel de support RP uniquement (aucune interaction avec le jeu).
"""

import random
from dataclasses import dataclass
from typing import Callable

import customtkinter as ctk

# ── Thème cyber ──────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

COLORS = {
    "bg": "#0a0e14",
    "panel": "#111820",
    "card": "#151c26",
    "card_hover": "#1a2332",
    "border": "#1e2a3a",
    "accent": "#00ff9f",
    "accent_dim": "#00b36e",
    "text": "#c8d6e5",
    "text_dim": "#6b7c93",
    "terminal_bg": "#050810",
    "success": "#00ff9f",
    "warning": "#ffb020",
    "error": "#ff4757",
    "scope_sur_place": "#ff4757",
    "scope_proximite": "#ffb020",
    "scope_distance": "#00ff9f",
}

FONT_MONO = ("Consolas", 12)
FONT_MONO_SM = ("Consolas", 10)
FONT_TITLE = ("Consolas", 22, "bold")
FONT_SUB = ("Consolas", 11)
FONT_BTN = ("Consolas", 13, "bold")
FONT_SCOPE = ("Consolas", 9, "bold")


@dataclass(frozen=True)
class Hack:
    name: str
    scope: str  # "SUR PLACE" | "À PROXIMITÉ" | "À DISTANCE"
    tool: str
    init_msg: str
    success_msg: str


HACKS: list[Hack] = [
    Hack(
        "Circuit Breaker",
        "SUR PLACE",
        "Extracteur de fusible & Bypass de relais fusibles",
        "[INIT] Connexion au tableau électrique… Scan des circuits actifs…",
        "Bypass relais actif — Circuit cible isolé. Alimentation coupée localement.",
    ),
    Hack(
        "Data Cracks",
        "À DISTANCE",
        "Antenne relais 4G/5G cryptée & Sniffer de paquets",
        "[INIT] Établissement du tunnel chiffré… Interception du flux de données…",
        "Sniffer actif — Paquets capturés et déchiffrés. Flux de données accessible.",
    ),
    Hack(
        "down&out.exe",
        "À DISTANCE",
        "Trojan injecté via serveur distant (Exploit zero-day)",
        "[INIT] Injection du payload zero-day… Contournement du pare-feu distant…",
        "down&out.exe déployé — Exploit zero-day actif. Système distant compromis.",
    ),
    Hack(
        "Hackconnect",
        "À PROXIMITÉ",
        "Boîtier de pontage Wi-Fi (Pineapple Nano)",
        "[INIT] Scan des réseaux Wi-Fi à proximité… Pontage du point d'accès cible…",
        "Pineapple Nano connecté — Pont Wi-Fi établi. Accès réseau local obtenu.",
    ),
    Hack(
        "brutforce.exe",
        "SUR PLACE",
        "Clé USB d'injection de dictionnaire (Rubber Ducky)",
        "[INIT] Insertion du vecteur USB… Chargement du dictionnaire…",
        "brutforce.exe en cours — Dictionnaire injecté. Tentatives de force brute lancées.",
    ),
    Hack(
        "Server Hack",
        "SUR PLACE",
        "Câble Ethernet RJ45 Cat 8 branché directement sur le rack du serveur",
        "[INIT] Liaison physique RJ45 établie… Énumération des services du rack…",
        "Accès rack confirmé — Connexion directe au serveur. Shell root disponible.",
    ),
    Hack(
        "VOLTlab",
        "SUR PLACE",
        "Multimètre connecté et modulateur de tension numérique",
        "[INIT] Calibration du multimètre… Analyse du schéma de tension…",
        "VOLTlab actif — Modulation de tension appliquée. Circuit reprogrammé.",
    ),
    Hack(
        "Fingerprint Cloner",
        "SUR PLACE",
        "Scanner optique de résidus de dactylogrammes (Cloneur d'empreintes)",
        "[INIT] Scan optique des résidus… Reconstruction du motif dactyloscopique…",
        "Fingerprint cloner actif — Correspondance trouvée à 100%.",
    ),
    Hack(
        "Voltage Hack",
        "À PROXIMITÉ",
        "Sonde à induction électromagnétique non intrusive",
        "[INIT] Activation de la sonde EM… Cartographie du champ électrique…",
        "Voltage Hack actif — Signature électrique identifiée. Override de tension possible.",
    ),
    Hack(
        "Dots / Keypad Hack",
        "SUR PLACE",
        "Caméra thermique portable (pour voir les touches chaudes) ou Décodeur de bus de données",
        "[INIT] Analyse thermique du clavier… Décodage du bus de données…",
        "Keypad compromis — Séquence de touches reconstituée. Code d'accès obtenu.",
    ),
    Hack(
        "Beam Hack",
        "À PROXIMITÉ",
        "Intercepteur de faisceau laser/optique ou Récepteur radiofréquence",
        "[INIT] Alignement de l'intercepteur… Capture du faisceau optique/RF…",
        "Beam Hack actif — Signal intercepté et décodé. Canal de communication ouvert.",
    ),
    Hack(
        "Hotwire Hack",
        "SUR PLACE",
        "Kit de démarrage électronique (Bypass de transpondeur OBD-II)",
        "[INIT] Connexion au port OBD-II… Bypass du transpondeur immobiliseur…",
        "Hotwire réussi — Transpondeur contourné. Démarrage du véhicule autorisé.",
    ),
    Hack(
        "Motherboard / Node Hacks",
        "SUR PLACE",
        "Pince IC Test Clip connectée directement sur la puce EEPROM de la carte mère",
        "[INIT] Connexion Test Clip sur EEPROM… Dump de la mémoire firmware…",
        "Node Hack actif — EEPROM dumpée. Firmware modifié et réinjecté.",
    ),
    Hack(
        "Safe Cracking",
        "SUR PLACE",
        "Stéthoscope électronique numérique à haute sensibilité (Analyseur de fréquences de goupilles)",
        "[INIT] Calibration du stéthoscope numérique… Analyse des fréquences de goupilles…",
        "Safe cracking en cours — 3/5 goupilles alignées. Ouverture imminente.",
    ),
    Hack(
        "Four Number Combination",
        "SUR PLACE",
        "Boîtier de Brute-Force mécanique ou Décodeur de signal de verrouillage",
        "[INIT] Brute-force mécanique initialisé… Décodage du signal de verrouillage…",
        "Combinaison trouvée — Code à 4 chiffres : ████ (masqué pour sécurité RP).",
    ),
]

SCOPE_COLORS = {
    "SUR PLACE": COLORS["scope_sur_place"],
    "À PROXIMITÉ": COLORS["scope_proximite"],
    "À DISTANCE": COLORS["scope_distance"],
}

SCOPE_LABELS = {
    "SUR PLACE": "[SUR PLACE]",
    "À PROXIMITÉ": "[À PROXIMITÉ]",
    "À DISTANCE": "[À DISTANCE]",
}


class HackCard(ctk.CTkFrame):
    """Carte cliquable représentant un hack."""

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        hack: Hack,
        on_click: Callable[[Hack], None],
        **kwargs,
    ):
        super().__init__(
            master,
            fg_color=COLORS["card"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=8,
            **kwargs,
        )
        self._hack = hack
        self._on_click = on_click
        self._hover = False

        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 4))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text=f"> {hack.name}",
            font=FONT_BTN,
            text_color=COLORS["accent"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        scope_color = SCOPE_COLORS.get(hack.scope, COLORS["text_dim"])
        ctk.CTkLabel(
            header,
            text=SCOPE_LABELS.get(hack.scope, f"[{hack.scope}]"),
            font=FONT_SCOPE,
            text_color=scope_color,
            fg_color="#1a1218" if hack.scope == "SUR PLACE" else "#1a1810" if hack.scope == "À PROXIMITÉ" else "#0a1a14",
            corner_radius=4,
            padx=6,
            pady=2,
        ).grid(row=0, column=1, sticky="e", padx=(8, 0))

        ctk.CTkLabel(
            self,
            text=f"Outil à brancher : {hack.tool}",
            font=FONT_MONO_SM,
            text_color=COLORS["text_dim"],
            anchor="w",
            wraplength=280,
            justify="left",
        ).grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))

        for widget in (self, header):
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<Button-1>", self._handle_click)
        for child in header.winfo_children():
            child.bind("<Enter>", self._on_enter)
            child.bind("<Leave>", self._on_leave)
            child.bind("<Button-1>", self._handle_click)
        self.bind("<Button-1>", self._handle_click)

    def _on_enter(self, _event=None):
        self._hover = True
        self.configure(fg_color=COLORS["card_hover"], border_color=COLORS["accent_dim"])

    def _on_leave(self, _event=None):
        self._hover = False
        self.configure(fg_color=COLORS["card"], border_color=COLORS["border"])

    def _handle_click(self, _event=None):
        self._on_click(self._hack)


class BingusHackPanel(ctk.CTk):
    """Fenêtre principale du panneau de contrôle Bingus."""

    BLINK_CYCLES = 8
    BLINK_INTERVAL_MS = 350

    def __init__(self):
        super().__init__()
        self.title("BINGUS // Hack Control Panel")
        self.geometry("920x720")
        self.minsize(800, 600)
        self.configure(fg_color=COLORS["bg"])

        self._hack_running = False
        self._blink_job: str | None = None
        self._blink_count = 0
        self._blink_on = True

        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # ── En-tête ──
        header = ctk.CTkFrame(self, fg_color=COLORS["panel"], corner_radius=0, height=72)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            header,
            text="◈ BINGUS",
            font=FONT_TITLE,
            text_color=COLORS["accent"],
        ).grid(row=0, column=0, padx=20, pady=16, sticky="w")

        ctk.CTkLabel(
            header,
            text="HACK CONTROL PANEL  //  RP VISUAL SUPPORT  //  v1.0",
            font=FONT_SUB,
            text_color=COLORS["text_dim"],
        ).grid(row=0, column=1, padx=10, pady=16, sticky="w")

        status_dot = ctk.CTkLabel(
            header,
            text="● ONLINE",
            font=FONT_SCOPE,
            text_color=COLORS["success"],
        )
        status_dot.grid(row=0, column=2, padx=20, pady=16, sticky="e")

        # ── Légende des portées ──
        legend = ctk.CTkFrame(self, fg_color=COLORS["panel"], corner_radius=0, height=36)
        legend.grid(row=1, column=0, sticky="ew")

        for i, (scope, color) in enumerate(SCOPE_COLORS.items()):
            ctk.CTkLabel(
                legend,
                text=f"{SCOPE_LABELS[scope]}  {scope.replace('À ', 'à ').title()}",
                font=FONT_SCOPE,
                text_color=color,
            ).pack(side="left", padx=(20 if i == 0 else 12, 0), pady=8)

        # ── Onglets par catégorie ──
        tabview = ctk.CTkTabview(
            self,
            fg_color=COLORS["panel"],
            segmented_button_fg_color=COLORS["card"],
            segmented_button_selected_color=COLORS["accent_dim"],
            segmented_button_selected_hover_color=COLORS["accent"],
            segmented_button_unselected_color=COLORS["card"],
            segmented_button_unselected_hover_color=COLORS["card_hover"],
            text_color=COLORS["text"],
        )
        tabview.grid(row=2, column=0, sticky="nsew", padx=12, pady=(8, 0))

        tabs = {
            "TOUS": tabview.add("  TOUS  "),
            "SUR PLACE": tabview.add(" SUR PLACE "),
            "À PROXIMITÉ": tabview.add(" PROXIMITÉ "),
            "À DISTANCE": tabview.add(" DISTANCE "),
        }

        for tab in tabs.values():
            tab.configure(fg_color=COLORS["panel"])
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_columnconfigure(1, weight=1)
            tab.grid_columnconfigure(2, weight=1)

        for idx, hack in enumerate(HACKS):
            target_tab = tabs["TOUS"]
            row, col = divmod(idx, 3)

            card = HackCard(target_tab, hack, self._start_hack)
            card.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)

        scope_indices: dict[str, list[int]] = {"SUR PLACE": [], "À PROXIMITÉ": [], "À DISTANCE": []}
        for idx, hack in enumerate(HACKS):
            scope_indices[hack.scope].append(idx)

        for scope, indices in scope_indices.items():
            tab = tabs[scope]
            for i, hack_idx in enumerate(indices):
                row, col = divmod(i, 3)
                card = HackCard(tab, HACKS[hack_idx], self._start_hack)
                card.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)

        # ── Zone terminal / statut ──
        console_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["terminal_bg"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=8,
        )
        console_frame.grid(row=3, column=0, sticky="ew", padx=12, pady=12)
        console_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            console_frame,
            text="▸ TERMINAL OUTPUT",
            font=FONT_SCOPE,
            text_color=COLORS["accent_dim"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(8, 0))

        self._status_label = ctk.CTkLabel(
            console_frame,
            text="En attente de sélection… Cliquez sur un hack pour lancer la simulation.",
            font=FONT_MONO,
            text_color=COLORS["text_dim"],
            anchor="w",
            wraplength=860,
            justify="left",
        )
        self._status_label.grid(row=1, column=0, sticky="ew", padx=12, pady=(4, 4))

        self._progress = ctk.CTkProgressBar(
            console_frame,
            fg_color=COLORS["card"],
            progress_color=COLORS["accent"],
            height=8,
        )
        self._progress.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 12))
        self._progress.set(0)

    def _set_status(self, text: str, color: str | None = None):
        self._status_label.configure(text=text, text_color=color or COLORS["text"])

    def _cancel_blink(self):
        if self._blink_job is not None:
            self.after_cancel(self._blink_job)
            self._blink_job = None

    def _start_blink(self, message: str):
        self._cancel_blink()
        self._blink_count = 0
        self._blink_on = True
        self._blink_message = message
        self._do_blink()

    def _do_blink(self):
        if self._blink_count >= self.BLINK_CYCLES * 2:
            self._set_status(f"✓ {self._blink_message}", COLORS["success"])
            self._blink_job = None
            self._hack_running = False
            return

        color = COLORS["success"] if self._blink_on else COLORS["terminal_bg"]
        prefix = "✓ SUCCESS // " if self._blink_on else "▸ "
        self._set_status(f"{prefix}{self._blink_message}", color)
        self._blink_on = not self._blink_on
        self._blink_count += 1
        self._blink_job = self.after(self.BLINK_INTERVAL_MS, self._do_blink)

    def _start_hack(self, hack: Hack):
        if self._hack_running:
            self._set_status("⚠ Opération en cours — veuillez patienter…", COLORS["warning"])
            return

        self._hack_running = True
        self._cancel_blink()
        self._progress.set(0)
        self._set_status(hack.init_msg, COLORS["accent"])

        duration = random.uniform(2.0, 5.0)
        self._animate_progress(duration, lambda: self._on_hack_complete(hack))

    def _animate_progress(self, duration: float, callback: Callable[[], None]):
        steps = 40
        interval_ms = int(duration * 1000 / steps)
        current = [0]

        def tick():
            current[0] += 1
            self._progress.set(current[0] / steps)
            if current[0] >= steps:
                callback()
            else:
                self.after(interval_ms, tick)

        tick()

    def _on_hack_complete(self, hack: Hack):
        self._progress.set(1)
        self._start_blink(hack.success_msg)


def main():
    app = BingusHackPanel()
    app.mainloop()


if __name__ == "__main__":
    main()
