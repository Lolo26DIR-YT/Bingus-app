import customtkinter as ctk


class FirewallBypassGame(ctk.CTkFrame):
    def __init__(self, parent, target, on_complete, profile=None, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_complete = on_complete
        self.expected_pattern = target.get("firewall_pattern", [True, False, True, True])
        self.switch_vars = [ctk.BooleanVar(value=False) for _ in self.expected_pattern]

        self.columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Mini-jeu : Contournement de pare-feu", font=ctk.CTkFont(size=18, weight="bold"), text_color="#66fcf1")
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        instruction = ctk.CTkLabel(
            self,
            text="Ajustez les bons commutateurs pour ouvrir une voie sécurisée à travers le pare-feu.",
            text_color="#c5c6c7",
            wraplength=700,
            justify="left",
        )
        instruction.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))

        switches_frame = ctk.CTkFrame(self, fg_color="#0b0f16")
        switches_frame.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 12))
        switches_frame.columnconfigure(tuple(range(len(self.switch_vars))), weight=1)

        for index, var in enumerate(self.switch_vars, start=1):
            switch = ctk.CTkCheckBox(
                switches_frame,
                text=f"Switch {index}",
                variable=var,
                onvalue=True,
                offvalue=False,
                text_color="#c5c6c7",
            )
            switch.grid(row=0, column=index - 1, sticky="ew", padx=4, pady=4)

        self.bypass_button = ctk.CTkButton(self, text="Bypass", command=self._attempt_bypass, fg_color="#45a29e")
        self.bypass_button.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 12))

        self.feedback = ctk.CTkLabel(self, text="", text_color="#8be9fd", wraplength=700, justify="left")
        self.feedback.grid(row=4, column=0, sticky="w", padx=12, pady=(0, 12))

    def _attempt_bypass(self):
        current_pattern = [var.get() for var in self.switch_vars]
        if current_pattern == self.expected_pattern:
            self.feedback.configure(text="Pare-feu contourné. Passage autorisé.")
            self.after(700, lambda: self.on_complete(True))
        else:
            self.feedback.configure(text="Configuration incorrecte. Ajustez les commutateurs.")
