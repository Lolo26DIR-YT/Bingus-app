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
        footer.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
        proceed_button = ctk.CTkButton(footer, text="Lancer le hack", command=self._proceed, fg_color="#45a29e")
        proceed_button.grid(row=0, column=1, sticky="ew", padx=(8, 0))

    def _proceed(self):
        self.proceed_callback(True)
        self.destroy()

    def _build_briefing_text(self, target, profile_name):
        # 1. Calcul de la durée
        base_duration = target.get("duration", 25) 
        total_duration = base_duration + 5
        real_duration = total_duration


        # 2. Gestion du risque au format X/5
        raw_risk = target.get("risk", 1)
        try:
            risk_val = int(raw_risk)
        except (ValueError, TypeError):
            risk_val = 1
        
        risk_str = f"{risk_val}/5"

        text = (
            f"--- RAPPORT DE BRIEFING OPERATIONNEL ---\n\n"
            f"Cible identifiée : {target.get('name', 'Inconnue')}\n"
            f"Profil : {profile_name}\n"
            f"Portée requise : {target.get('distance_label', 'Inconnue')}\n"
            f"Niveau de risque : {risk_str}\n"
            f"Temps de traitement requis : {real_duration} secondes\n\n"
            f"Matériel RP requis :\n"
        )
        
        tools = target.get("tools", [])
        if tools:
            for tool in tools:
                text += f" - {tool}\n"
        else:
            text += f" - Aucun matériel spécifique requis\n"
            
        text += (
            f"\nDescription de la mission :\n"
            f"{target.get('rp_description', 'Aucune description disponible.')}\n"
        )
        return text