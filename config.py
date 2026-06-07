APP_TITLE = "Bingus Hack Simulator"
APP_SIZE = "1280x780"
FONT_FAMILY = "JetBrains Mono"

# Colors
BG_COLOR = "#0b0c10"
PANEL_BG = "#131820"
SURFACE_BG = "#1f2833"
FOREGROUND_COLOR = "#c5c6c7"
SECONDARY_TEXT = "#66fcf1"
PRIMARY_COLOR = "#45a29e"
ACCENT_COLOR = "#66fcf1"
DANGER_COLOR = "#ff5555"
SUCCESS_COLOR = "#50fa7b"
WARNING_COLOR = "#f1fa8c"

DISTANCE_LEVELS = [
    {"level": 1, "label": "🔴 PROXIMITÉ IMMÉDIATE", "description": "≤ 2 mètres — contact physique requis"},
    {"level": 2, "label": "🟠 COURTE PORTÉE", "description": "≤ 15 mètres — ligne de vue directe"},
    {"level": 3, "label": "🟡 PORTÉE MOYENNE", "description": "≤ 50 mètres — antenne directionnelle requise"},
    {"level": 4, "label": "🟢 LONGUE PORTÉE", "description": "≤ 500 mètres — équipement spécialisé requis"},
    {"level": 5, "label": "🔵 PORTÉE ÉTENDUE", "description": "≤ 2 km — relais réseau ou drone requis"},
    {"level": 6, "label": "🟣 SAN ANDREAS COMPLET", "description": "N'importe où dans l'État de San Andreas"},
    {"level": 7, "label": "⚪ SAN ANDREAS + ROBADA", "description": "Couverture maximale — infrastructure fédérale"},
]

OPERATOR_PROFILES = [
    {"name": "Novice", "modifier": 1.2, "description": "Apprenti hackeur, les actions prennent plus de temps."},
    {"name": "Intermédiaire", "modifier": 1.0, "description": "Compétent et stable, bon équilibre entre vitesse et précision."},
    {"name": "Expert", "modifier": 0.85, "description": "Rapidement opérationnel avec de l'expérience."},
    {"name": "Ghost", "modifier": 0.7, "description": "Maître furtif, exécute les hacks comme une ombre."},
]

TOOL_GLOSSARY = {
    "Laptop": "Ordinateur portable hacké, OS modifié, outils pré-installés",
    "Flipper Zero": "Multi-outil radio : RFID, NFC, IR, Sub-GHz, signal replay",
    "RFID Cloner": "Clone les badges et cartes d'accès magnétiques / RFID",
    "WiFi Pineapple": "Crée de faux points d'accès WiFi, capture trafic réseau",
    "OBD Dongle": "Accès au port OBD-II d'un véhicule pour lecture/écriture",
    "SDR Antenna": "Radio Définie par Logiciel — écoute et analyse les fréquences",
    "RF Jammer": "Brouille les fréquences radio dans un rayon défini",
    "GPS Spoofer": "Envoie de fausses coordonnées GPS à une cible",
    "Directional Antenna": "Antenne Yagi directionnelle — étend la portée WiFi / RF",
    "Ethernet Tap": "Écoute passive sur un câble réseau physique",
    "4G Modem": "Connexion mobile anonymisée via carte SIM jetable",
    "VPN Relay": "Tunnel chiffré pour masquer l'origine de l'attaque",
    "Serveur VPS": "Serveur distant loué pour relayer et anonymiser l'attaque",
    "Serveur Relay": "Infrastructure intermédiaire pour les attaques longue portée",
    "ATM Skimmer": "Dispositif physique de clonage de cartes bancaires",
    "Card Skimmer": "Version portable pour TPE et bornes de paiement NFC",
    "Thermal Camera": "Caméra thermique détectant les touches récemment pressées",
    "Signal Analyser": "Analyse le spectre électromagnétique d'un appareil",
    "SCADA Kit": "Outils d'exploitation des systèmes industriels",
    "Bypass Kit": "Ensemble d'outils pour court-circuiter les serrures électroniques",
    "0-Day Kit": "Exploitation de failles inconnues — niveau maximum",
    "Botnet": "Réseau de machines compromises pour amplifier l'attaque",
    "Decoder": "Déchiffrement de protocoles radio propriétaires",
    "Fiber Tap": "Interception physique d'un câble fibre optique",
    "Insider": "Complice interne ayant un accès légitime (élément RP)",
}

RISK_SUMMARY = {
    1: "Faible",
    2: "Modéré",
    3: "Important",
    4: "Élevé",
    5: "Critique",
}
