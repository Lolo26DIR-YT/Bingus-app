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
        self.inventory = set()

        # Structure principale de la grille globale
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, minsize=320)
        self.grid_columnconfigure(1, weight=1)

        # --- STYLE DES PANNEAUX ---
        
        # Le Header avec une fine bordure cyan
        self.header = ctk.CTkFrame(self, fg_color="#131820", border_width=1, border_color="#45a29e")
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 10))
        self.header.columnconfigure(0, weight=1)
        self.header.columnconfigure(1, weight=0)
        self.header.columnconfigure(2, weight=0)

        header_label = ctk.CTkLabel(
            self.header,
            text=APP_TITLE,
            font=ctk.CTkFont(family="JetBrains Mono", size=18, weight="bold"),
            text_color="#66fcf1",
        )
        header_label.grid(row=0, column=0, sticky="w", padx=15, pady=12)

        home_button = ctk.CTkButton(self.header, text="Accueil", command=self.show_home, fg_color="#1f2833", hover_color="#45a29e")
        home_button.grid(row=0, column=1, sticky="e", padx=(0, 8), pady=12)
        inventory_button = ctk.CTkButton(self.header, text="Inventaire", command=self.show_inventory, fg_color="#45a29e", hover_color="#66fcf1", text_color="#0b0c10")
        inventory_button.grid(row=0, column=2, sticky="e", padx=(0, 12), pady=12)

        # La Sidebar (Correction ici : on passe juste "self" comme premier argument)
        self.sidebar = Sidebar(
            self,
            categories=CATEGORIES,
            on_category_selected=self.on_category_selected,
            on_target_selected=self.on_target_selected,
        )
        self.sidebar.configure(border_width=1, border_color="#1f2833")
        self.sidebar.grid(row=1, column=0, sticky="nsew", padx=(16, 8), pady=6)

        # Le Panneau Principal (Correction ici aussi)
        self.main_panel = MainPanel(
            self,
            on_start_hack=self.on_start_hack,
            on_request_log=self.add_log,
            on_show_inventory=self.show_inventory,
            on_toggle_sidebar=self.set_sidebar_visible,
            inventory=self.inventory,
        )
        self.main_panel.grid(row=1, column=1, sticky="nsew", padx=(8, 16), pady=6)

        # Le Panneau de Logs
        self.log_panel = LogPanel(self)
        self.log_panel.configure(border_width=1, border_color="#45a29e")
        self.log_panel.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=16, pady=(10, 16))

        self.sidebar.select_category(self.selected_category["key"])
        self.main_panel.show_home_page()
        self.add_log("Bingus Hack Simulator démarré.")

    def show_home(self):
        self.set_sidebar_visible(False)
        self.main_panel.show_home_page()
        self.add_log("Retour à l'accueil.")

    def show_inventory(self):
        self.sidebar.grid()
        self.main_panel.show_inventory_page()
        self.add_log("Ouverture de l'inventaire.")

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

    def on_start_hack(self, target):
        self.add_log(f"Préparation du hacking : {target['name']}")
        self.main_panel.start_hack(target, self.profile_name)

    def add_log(self, message):
        self.log_panel.add_log(message)


def run_app():
    app = HackerSimulatorApp()
    app.mainloop()

if __name__ == "__main__":
    run_app()