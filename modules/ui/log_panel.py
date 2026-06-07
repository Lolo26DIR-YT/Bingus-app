import customtkinter as ctk


class LogPanel(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.columnconfigure(0, weight=1)
        label = ctk.CTkLabel(self, text="Journal des opérations", font=ctk.CTkFont(size=14, weight="bold"), text_color="#66fcf1")
        label.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.textbox = ctk.CTkTextbox(self, width=0, height=200, wrap="word", fg_color="#0b0c10", text_color="#c5c6c7", corner_radius=8)
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.textbox.configure(state="disabled")

    def add_log(self, message):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"[{self._timestamp()}] {message}\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def _timestamp(self):
        from datetime import datetime

        return datetime.now().strftime("%H:%M:%S")
