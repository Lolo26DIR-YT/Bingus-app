import customtkinter as ctk
from config import APP_TITLE, APP_SIZE, BG_COLOR, PANEL_BG, FOREGROUND_COLOR, SECONDARY_TEXT, ACCENT_COLOR, OPERATOR_PROFILES
from modules.targets import CATEGORIES
from modules.ui.sidebar import Sidebar
from modules.ui.main_panel import MainPanel
from modules.ui.log_panel import LogPanel
from modules.ui.profile_panel import ProfilePanel


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
        self.profile_name = OPERATOR_PROFILES[1]["name"]

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = Sidebar(
            self,
            categories=CATEGORIES,
            on_category_selected=self.on_category_selected,
            on_target_selected=self.on_target_selected,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)

        self.main_panel = MainPanel(self, on_start_hack=self.on_start_hack, on_request_log=self.add_log)
        self.main_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=16)

        self.profile_panel = ProfilePanel(
            self,
            profiles=OPERATOR_PROFILES,
            initial_profile=self.profile_name,
            on_profile_changed=self.on_profile_changed,
        )
        self.profile_panel.grid(row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 16))

        self.log_panel = LogPanel(self)
        self.log_panel.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=16, pady=(0, 16))
        self.grid_rowconfigure(2, weight=0)

        self.sidebar.select_category(self.selected_category["key"])
        self.main_panel.show_placeholder()
        self.add_log("Bingus Hack Simulator démarré.")

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

    def on_profile_changed(self, profile_name):
        self.profile_name = profile_name
        self.add_log(f"Profil opérateur activé : {profile_name}")
        self.profile_panel.update_description(profile_name)

    def add_log(self, message):
        self.log_panel.add_log(message)


def run_app():
    app = HackerSimulatorApp()
    app.mainloop()


if __name__ == "__main__":
    run_app()
