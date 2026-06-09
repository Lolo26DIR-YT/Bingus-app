import customtkinter as ctk
from config import APP_TITLE, APP_SIZE, BG_COLOR
from modules.targets import CATEGORIES
from modules.ui.sidebar import Sidebar
from modules.ui.main_panel import MainPanel
from modules.ui.log_panel import LogPanel

def create_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

class HackerSimulatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        create_theme()
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.configure(fg_color=BG_COLOR)

        self.selected_category = CATEGORIES[0]
        self.selected_target = None
        self.profile_name = "Intermédiaire"

        # Structure principale de la grille globale
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, minsize=320)
        self.grid_columnconfigure(1, weight=1)

        # --- STYLE DES PANNEAUX ---\n        
        # Le Header avec une fine bordure cyan
        self.header = ctk.CTkFrame(self, fg_color="#131820", border_width=1, border_color="#45a29e")
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 10))
        self.header.grid_propagate(False)
        self.header.configure(height=65)

        # Grille du Header
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(1, weight=0)
        self.header.grid_rowconfigure(0, weight=1)

        # Titre du Header (Style Matrix/Cyber)
        self.header_title = ctk.CTkLabel(
            self.header, 
            text="BINGUS HACKING SYSTEM v1.4", 
            font=ctk.CTkFont(family="Courier", size=18, weight="bold"), 
            text_color="#66fcf1"
        )
        self.header_title.grid(row=0, column=0, sticky="w", padx=16)

        # Le Panneau Principal (MainPanel)
        self.main_panel = MainPanel(
            self, 
            on_request_log=self.add_log,
            on_start_hack=self.on_start_hack,
            on_toggle_sidebar=None
        )
        self.main_panel.configure(border_width=1, border_color="#45a29e")
        self.main_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 16), pady=6)

        # La Sidebar à gauche
        self.sidebar = Sidebar(
            self, 
            categories=CATEGORIES, 
            on_category_selected=self.on_category_selected,
            on_target_selected=self.on_target_selected
        )
        self.sidebar.configure(border_width=1, border_color="#45a29e")
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=(16, 10), pady=6)

        # Le Panneau de Logs
        self.log_panel = LogPanel(self)
        self.log_panel.configure(border_width=1, border_color="#45a29e")
        self.log_panel.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=16, pady=(10, 16))

        # Initialisation par défaut : On force la sélection de la première cible de la première catégorie
        self.sidebar.select_category(self.selected_category["key"])
        if "targets" in self.selected_category and len(self.selected_category["targets"]) > 0:
            first_target = self.selected_category["targets"][0]
            self.on_target_selected(first_target)
            
        self.add_log("Bingus Hack Simulator démarré - Système opérationnel.")

    def set_sidebar_visible(self, visible: bool):
        if visible:
            self.sidebar.grid()
        else:
            self.sidebar.grid_remove()

    def on_category_selected(self, category):
        self.selected_category = category
        self.add_log(f"Catégorie sélectionnée : {category['label']}")

    def on_target_selected(self, target):
        self.selected_target = target
        self.main_panel.show_target(target)
        self.add_log(f"Cible sélectionnée : {target['name']} ({target['distance_label']})")

    def on_start_hack(self, target, profile):
        self.add_log(f"Lancement du piratage sur {target['name']} avec le profil {profile}")

    def add_log(self, text: str):
        if hasattr(self, 'log_panel'):
            self.log_panel.add_log(text)

def run_app():
    app = HackerSimulatorApp()
    app.mainloop()

if __name__ == "__main__":
    run_app()