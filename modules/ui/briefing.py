import customtkinter as ctk


class BriefingDialog(ctk.CTkToplevel):
    def __init__(self, parent, target, profile_name, proceed_callback):
        super().__init__(parent)
        self.title("Briefing de mission")
        self.geometry("520x420")
        self.configure(fg_color="#131820")
        self.proceed_callback = proceed_callback

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header = ctk.CTkLabel(self, text="Briefing de la cible", font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        header.grid(row=0, column=0, padx=20, pady=(20, 12), sticky="w")

        description = ctk.CTkTextbox(self, width=480, height=260, fg_color="#0b0c10", text_color="#c5c6c7", corner_radius=12)
        description.grid(row=1, column=0, padx=20, pady=(0, 12), sticky="nsew")
        description.insert("0.0", self._build_briefing_text(target, profile_name))
        description.configure(state="disabled")

        footer = ctk.CTkFrame(self, fg_color="#0b0c10")
        footer.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        footer.columnconfigure((0, 1), weight=1)

        cancel_button = ctk.CTkButton(footer, text="Annuler", command=self._cancel, fg_color="#282a36", hover_color="#44475a")
        cancel_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        proceed_button = ctk.CTkButton(footer, text="Lancer le hack", command=self._proceed, fg_color="#45a29e")
        proceed_button.grid(row=0, column=1, sticky="ew", padx=(8, 0))

    def _build_briefing_text(self, target, profile_name):
        return (
            f"🎯 CIBLE : {target['name']}\n"
            f"📍 DISTANCE REQUISE : {target['distance_label']}\n"
            f"🔴 NIVEAU DE RISQUE : {target['risk']}/5\n"
            f"⏱️ DURÉE ESTIMÉE : {target['duration']} secondes\n\n"
            f"🧰 OUTILS REQUIS :\n"
            + "\n".join([f"  • {tool}" for tool in target["tools"]])
            + "\n\n"
            f"Profil opérateur : {profile_name}\n"
            f"Interaction attendue : {target['interaction']}\n\n"
            f"Résumé : {target['rp_description']}"
        )

    def _proceed(self):
        self.proceed_callback(True)
        self.destroy()

    def _cancel(self):
        self.proceed_callback(False)
        self.destroy()
