import customtkinter as ctk


class ProfilePanel(ctk.CTkFrame):
    def __init__(self, parent, profiles, initial_profile, on_profile_changed, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.profiles = profiles
        self.on_profile_changed = on_profile_changed

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        profile_label = ctk.CTkLabel(self, text="Profil opérateur", font=ctk.CTkFont(size=14, weight="bold"), text_color="#66fcf1")
        profile_label.grid(row=0, column=0, sticky="w", padx=12, pady=12)

        self.profile_menu = ctk.CTkOptionMenu(
            self,
            values=[profile["name"] for profile in profiles],
            command=self._profile_changed,
            fg_color="#0b0c10",
            button_color="#1f2833",
            dropdown_fg_color="#0b0c10",
            text_color="#c5c6c7",
        )
        self.profile_menu.set(initial_profile)
        self.profile_menu.grid(row=0, column=1, sticky="e", padx=12, pady=12)

        self.description_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12), text_color="#c5c6c7", wraplength=980, justify="left")
        self.description_label.grid(row=1, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 12))
        self.update_description(initial_profile)

    def _profile_changed(self, value):
        self.on_profile_changed(value)
        self.update_description(value)

    def update_description(self, profile_name):
        selected = next((profile for profile in self.profiles if profile["name"] == profile_name), None)
        if selected:
            self.description_label.configure(text=f"{selected['description']} — Modificateur de durée : {selected['modifier']}x")
